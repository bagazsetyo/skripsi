import { useQueries } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboardApi";

export function useDashboardOverview() {
  const [datasetQuery, modelsQuery, runsQuery, activeModelQuery] = useQueries({
    queries: [
      { queryKey: ["dashboard", "dataset-summary"], queryFn: dashboardApi.getDatasetSummary },
      { queryKey: ["dashboard", "models"], queryFn: dashboardApi.getModels },
      { queryKey: ["dashboard", "training-runs"], queryFn: dashboardApi.getTrainingRuns },
      { queryKey: ["dashboard", "active-model"], queryFn: dashboardApi.getActiveModel, retry: false },
    ],
  });

  return {
    datasetSummary: datasetQuery.data ?? null,
    models: modelsQuery.data ?? [],
    trainingRuns: runsQuery.data ?? [],
    activeModel: activeModelQuery.data ?? null,
    isLoading:
      datasetQuery.isLoading ||
      modelsQuery.isLoading ||
      runsQuery.isLoading ||
      activeModelQuery.isLoading,
    isError: datasetQuery.isError || modelsQuery.isError || runsQuery.isError,
    errors: [datasetQuery.error, modelsQuery.error, runsQuery.error].filter(Boolean),
    refetchAll: () => {
      datasetQuery.refetch();
      modelsQuery.refetch();
      runsQuery.refetch();
      activeModelQuery.refetch();
    },
  };
}
