import { useMutation, useQuery } from "@tanstack/react-query";
import { message } from "antd";
import { predictionApi } from "../api/predictionApi";

export function usePredictionWorkspace() {
  const activeModelQuery = useQuery({
    queryKey: ["prediction", "active-model"],
    queryFn: predictionApi.getActiveModel,
    retry: false,
  });

  const predictMutation = useMutation({
    mutationFn: predictionApi.predictImage,
    onError: (error) => {
      message.error(error?.message || "Prediksi gagal dijalankan");
    },
  });

  return {
    activeModel: activeModelQuery.data ?? null,
    isLoadingModel: activeModelQuery.isLoading,
    isErrorModel: activeModelQuery.isError,
    modelError: activeModelQuery.error,
    refetchModel: activeModelQuery.refetch,
    runPrediction: predictMutation.mutateAsync,
    predictionResult: predictMutation.data ?? null,
    isPredicting: predictMutation.isPending,
    resetPrediction: predictMutation.reset,
  };
}
