import { getApiBaseUrl } from "@/lib/env";
import type { ErrorCode, ErrorResponse } from "@/types/word";
import { errorResponseSchema } from "@/types/word.schemas";
import { z } from "zod";

type PrimitiveQueryValue = string | number | boolean | null | undefined;
type AnySchema = z.ZodTypeAny;

export type ApiRequestOptions<TSchema extends AnySchema = AnySchema> = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  query?: Record<string, PrimitiveQueryValue>;
  cache?: RequestCache;
  next?: NextFetchRequestConfig;
  headers?: HeadersInit;
  schema?: TSchema;
};

const ERROR_MESSAGES: Record<ErrorCode, string> = {
  application_error: "Unexpected application error.",
  database_connection_error: "Database is temporarily unavailable.",
  integration_error: "External service error.",
  openai_configuration_error: "OpenAI is not configured correctly.",
  openai_rate_limit: "OpenAI rate limit exceeded. Please try again later.",
  openai_response_format_error: "OpenAI returned invalid structured data.",
  openai_unavailable: "OpenAI service is temporarily unavailable.",
  persistence_error: "Database operation failed.",
  request_validation_error: "Request validation failed.",
  validation_error: "Invalid input data.",
  word_already_exists: "This word already exists for the selected direction.",
  word_not_found: "Word not found.",
  unknown_error: "Request failed.",
};

export class ApiClientError extends Error {
  status: number;
  errorCode: ErrorCode | string;
  details: ErrorResponse | null;

  constructor(params: {
    message: string;
    status: number;
    errorCode: ErrorCode | string;
    details: ErrorResponse | null;
  }) {
    super(params.message);
    this.name = "ApiClientError";
    this.status = params.status;
    this.errorCode = params.errorCode;
    this.details = params.details;
  }
}

export class ApiContractError extends ApiClientError {
  issues: z.ZodIssue[];
  payload: unknown;

  constructor(params: {
    status: number;
    payload: unknown;
    issues: z.ZodIssue[];
  }) {
    super({
      message: "API response did not match the expected contract.",
      status: params.status,
      errorCode: "unknown_error",
      details: null,
    });
    this.name = "ApiContractError";
    this.issues = params.issues;
    this.payload = params.payload;
  }
}

function buildUrl(path: string, query?: Record<string, PrimitiveQueryValue>) {
  const baseUrl = getApiBaseUrl();
  const url = new URL(path, baseUrl);

  if (!query) {
    return url.toString();
  }

  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === "") {
      continue;
    }

    url.searchParams.set(key, String(value));
  }

  return url.toString();
}

async function parseJsonSafely<T>(response: Response): Promise<T | null> {
  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.includes("application/json")) {
    return null;
  }

  try {
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export function normalizeApiError(status: number, error: ErrorResponse | null) {
  const errorCode = error?.error_code ?? "unknown_error";
  const fallbackMessage = ERROR_MESSAGES[errorCode as ErrorCode] ?? ERROR_MESSAGES.unknown_error;

  return new ApiClientError({
    message: error?.detail || fallbackMessage,
    status,
    errorCode,
    details: error,
  });
}

export async function request<TSchema extends AnySchema>(
  path: string,
  options: ApiRequestOptions<TSchema> & { schema: TSchema },
): Promise<z.infer<TSchema>>;
export async function request<T>(
  path: string,
  options?: ApiRequestOptions,
): Promise<T>;
export async function request<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const response = await fetch(buildUrl(path, options.query), {
    method: options.method ?? "GET",
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
    cache: options.cache ?? "no-store",
    next: options.next,
  });

  if (!response.ok) {
    const errorPayload = await parseJsonSafely<unknown>(response);
    const parsedError = errorResponseSchema.safeParse(errorPayload);
    throw normalizeApiError(response.status, parsedError.success ? parsedError.data : null);
  }

  const data = await parseJsonSafely<unknown>(response);

  if (data === null) {
    throw new ApiClientError({
      message: "Expected a JSON response but received a different payload.",
      status: response.status,
      errorCode: "unknown_error",
      details: null,
    });
  }

  if (options.schema) {
    const parsed = options.schema.safeParse(data);

    if (!parsed.success) {
      throw new ApiContractError({
        status: response.status,
        payload: data,
        issues: parsed.error.issues,
      });
    }

    return parsed.data as T;
  }

  return data as T;
}
