import { useMutation, useQueries } from "@tanstack/react-query";
import { message } from "antd";
import { datasetApi } from "../api/datasetApi";

export function useDatasetOverview() {
  const [classesQuery, summaryQuery, validationQuery] = useQueries({
    queries: [
      { queryKey: ["dataset", "classes"], queryFn: datasetApi.getClasses },
      { queryKey: ["dataset", "summary"], queryFn: datasetApi.getSummary },
      { queryKey: ["dataset", "validation"], queryFn: datasetApi.getValidation },
    ],
  });

  const refreshCacheMutation = useMutation({
    mutationFn: datasetApi.refreshCache,
    onSuccess: (response) => {
      const isRunning = response?.status === "running";
      message.success(
        isRunning
          ? "Refresh dataset sedang berjalan di background"
          : "Refresh dataset dimulai di background"
      );
    },
    onError: (error) => {
      message.error(error?.message || "Gagal memperbarui cache dataset");
    },
  });

  return {
    classes: classesQuery.data ?? [],
    summary: summaryQuery.data ?? null,
    validation: validationQuery.data ?? null,
    isLoading: classesQuery.isLoading || summaryQuery.isLoading || validationQuery.isLoading,
    isError: classesQuery.isError || summaryQuery.isError || validationQuery.isError,
    errors: [classesQuery.error, summaryQuery.error, validationQuery.error].filter(Boolean),
    refetchAll: () => {
      classesQuery.refetch();
      summaryQuery.refetch();
      validationQuery.refetch();
    },
    refreshDatasetCache: refreshCacheMutation.mutateAsync,
    isRefreshingDatasetCache: refreshCacheMutation.isPending,
  };
}
