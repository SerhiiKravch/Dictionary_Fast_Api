"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";

import { Button } from "@/components/ui/button";

type PaginationProps = {
  total: number;
  limit: number;
  offset: number;
};

export function Pagination({ total, limit, offset }: PaginationProps) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  if (total <= limit) {
    return null;
  }

  const previousOffset = Math.max(offset - limit, 0);
  const nextOffset = offset + limit;
  const hasPrevious = offset > 0;
  const hasNext = nextOffset < total;

  function navigate(nextValue: number) {
    const params = new URLSearchParams(searchParams.toString());
    params.set("offset", String(nextValue));
    params.set("limit", String(limit));
    router.push(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="pagination">
      <Button type="button" disabled={!hasPrevious} onClick={() => navigate(previousOffset)}>
        Previous
      </Button>
      <span className="pagination__label">
        {offset + 1}-{Math.min(offset + limit, total)} of {total}
      </span>
      <Button type="button" disabled={!hasNext} onClick={() => navigate(nextOffset)}>
        Next
      </Button>
    </div>
  );
}
