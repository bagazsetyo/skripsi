import { useMutation, useQueries, useQueryClient } from "@tanstack/react-query";
import { message } from "antd";
import { trainingApi } from "../api/trainingApi";

export function useTrainingWorkspace() {
  const queryClient = useQueryClient();

  const [configQuery, runsQuery, modelsQuery, activeModelQuery] = useQueries({
    queries: [
      { queryKey: ["training", "config"], queryFn: trainingApi.getConfig },
      { queryKey: ["training", "runs"], queryFn: trainingApi.getRuns, refetchInterval: 10_000 },
      { queryKey: ["models"], queryFn: trainingApi.getModels, refetchInterval: 10_000 },
      { queryKey: ["models", "active"], queryFn: trainingApi.getActiveModel, retry: false, refetchInterval: 10_000 },
    ],
  });

  const createRunMutation = useMutation({
    mutationFn: trainingApi.createRun,
    onSuccess: () => {
      message.success("Training run berhasil dibuat");
      queryClient.invalidateQueries({ queryKey: ["training", "runs"] });
      queryClient.invalidateQueries({ queryKey: ["models"] });
    },
    onError: (error) => {
      message.error(error?.message || "Gagal membuat training run");
    },
  });

  const activateModelMutation = useMutation({
    mutationFn: trainingApi.activateModel,
    onSuccess: () => {
      message.success("Model aktif berhasil diperbarui");
      queryClient.invalidateQueries({ queryKey: ["models"] });
      queryClient.invalidateQueries({ queryKey: ["models", "active"] });
    },
    onError: (error) => {
      message.error(error?.message || "Gagal mengaktifkan model");
    },
  });

  return {
    config: configQuery.data ?? null,
    runs: runsQuery.data ?? [],
    models: modelsQuery.data ?? [],
    activeModel: activeModelQuery.data ?? null,
    isLoading:
      configQuery.isLoading ||
      runsQuery.isLoading ||
      modelsQuery.isLoading ||
      activeModelQuery.isLoading,
    isError:
      configQuery.isError ||
      runsQuery.isError ||
      modelsQuery.isError,
    errors: [configQuery.error, runsQuery.error, modelsQuery.error].filter(Boolean),
    createRun: createRunMutation.mutateAsync,
    isCreatingRun: createRunMutation.isPending,
    activateModel: activateModelMutation.mutateAsync,
    isActivatingModel: activateModelMutation.isPending,
    refetchAll: () => {
      configQuery.refetch();
      runsQuery.refetch();
      modelsQuery.refetch();
      activeModelQuery.refetch();
    },
  };
}
