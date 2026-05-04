import { useMutation, useQueries, useQueryClient } from "@tanstack/react-query";
import { message } from "antd";
import { datasetApi } from "../api/datasetApi";

export function useDatasetOverview() {
  const queryClient = useQueryClient();
  const [classesQuery, summaryQuery, validationQuery] = useQueries({
    queries: [
      { queryKey: ["dataset", "classes"], queryFn: datasetApi.getClasses },
      { queryKey: ["dataset", "summary"], queryFn: datasetApi.getSummary },
      { queryKey: ["dataset", "validation"], queryFn: datasetApi.getValidation },
    ],
  });

  const refreshCacheMutation = useMutation({
    mutationFn: datasetApi.refreshCache,
    onSuccess: async () => {
      message.success("Cache dataset berhasil diperbarui");
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["dataset", "summary"] }),
        queryClient.invalidateQueries({ queryKey: ["dataset", "validation"] }),
      ]);
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
