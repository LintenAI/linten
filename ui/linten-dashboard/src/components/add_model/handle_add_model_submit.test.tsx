import { describe, expect, it, vi } from "vitest";
import { prepareModelAddRequest } from "./handle_add_model_submit";

vi.mock("../networking", () => ({
  modelCreateCall: vi.fn(),
}));

describe("prepareModelAddRequest", () => {
  it("returns deployment data for the most basic form", async () => {
    const formValues = {
      model_mappings: [
        {
          public_name: "Public Model",
          linten_model: "linten/public",
        },
      ],
      model_name: "custom-model-name",
      base_model: "gpt-4",
      team_id: "team-123",
      model_access_group: ["group-1"],
      input_cost_per_token: "2000000",
      output_cost_per_token: "1000000",
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.modelName).toBe("Public Model");
    expect(deployment.lintenParamsObj.model).toBe("custom-model-name");
    expect(deployment.lintenParamsObj.input_cost_per_token).toBe(2);
    expect(deployment.lintenParamsObj.output_cost_per_token).toBe(1);
    expect(deployment.modelInfoObj.base_model).toBe("gpt-4");
    expect(deployment.modelInfoObj.access_groups).toEqual(["group-1"]);
    expect(deployment.modelInfoObj.team_id).toBe("team-123");
  });

  it("converts both cache write tiers from per-million to per-token", async () => {
    const formValues = {
      model_mappings: [{ public_name: "claude-sonnet", linten_model: "anthropic/claude-sonnet-4-6" }],
      model_name: "anthropic/claude-sonnet-4-6",
      custom_pricing: true,
      input_cost_per_token: "3",
      output_cost_per_token: "15",
      cache_creation_input_token_cost: "3.75",
      cache_creation_input_token_cost_above_1hr: "6",
    };

    const [deployment] = (await prepareModelAddRequest({ ...formValues }, "token", null))!;

    expect(deployment.lintenParamsObj.cache_creation_input_token_cost).toBeCloseTo(0.00000375, 12);
    expect(deployment.lintenParamsObj.cache_creation_input_token_cost_above_1hr).toBeCloseTo(0.000006, 12);
  });

  it("converts the pricing once when several models are added together", async () => {
    const formValues = {
      model_mappings: [
        { public_name: "claude-sonnet", linten_model: "anthropic/claude-sonnet-4-6" },
        { public_name: "claude-opus", linten_model: "anthropic/claude-opus-4-2" },
      ],
      model_name: "anthropic/claude-sonnet-4-6",
      custom_pricing: true,
      input_cost_per_token: "3",
      cache_creation_input_token_cost: "3.75",
      cache_creation_input_token_cost_above_1hr: "6",
    };

    const deployments = (await prepareModelAddRequest({ ...formValues }, "token", null))!;

    expect(deployments).toHaveLength(2);
    for (const deployment of deployments) {
      expect(deployment.lintenParamsObj.input_cost_per_token).toBeCloseTo(0.000003, 12);
      expect(deployment.lintenParamsObj.cache_creation_input_token_cost).toBeCloseTo(0.00000375, 12);
      expect(deployment.lintenParamsObj.cache_creation_input_token_cost_above_1hr).toBeCloseTo(0.000006, 12);
    }
  });

  it("leaves the 1 hour cache write tier unset when its field is blank", async () => {
    const formValues = {
      model_mappings: [{ public_name: "claude-sonnet", linten_model: "anthropic/claude-sonnet-4-6" }],
      model_name: "anthropic/claude-sonnet-4-6",
      custom_pricing: true,
      cache_creation_input_token_cost: "3.75",
      cache_creation_input_token_cost_above_1hr: "",
    };

    const [deployment] = (await prepareModelAddRequest({ ...formValues }, "token", null))!;

    expect(deployment.lintenParamsObj).not.toHaveProperty("cache_creation_input_token_cost_above_1hr");
    expect(deployment.lintenParamsObj.cache_creation_input_token_cost).toBeCloseTo(0.00000375, 12);
  });

  it("uses a lowercase fallback for unrecognized custom providers", async () => {
    const fallbackValues = {
      model_mappings: [
        {
          public_name: "Petals Model",
          linten_model: "petals/model",
        },
      ],
      model_name: "petals/model",
      custom_llm_provider: "Petals",
    };

    const deployments = await prepareModelAddRequest({ ...fallbackValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.lintenParamsObj.custom_llm_provider).toBe("petals");
  });

  it("sends the backend's own slug for a provider whose key is spelled differently in provider_map", async () => {
    const formValues = {
      model_mappings: [{ public_name: "Composer", linten_model: "cursor/composer-1" }],
      model_name: "cursor/composer-1",
      custom_llm_provider: "CURSOR",
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments![0].lintenParamsObj.custom_llm_provider).toBe("cursor");
  });

  it("builds the wildcard model from the backend slug, not the raw dropdown key", async () => {
    const formValues = {
      model: ["all-wildcard"],
      custom_llm_provider: "CURSOR",
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.modelName).toBe("cursor/*");
    expect(deployment.lintenParamsObj.model).toBe("cursor/*");
  });

  it("ignores linten_credential_name inside Linten Params JSON", async () => {
    const formValues = {
      model_mappings: [
        {
          public_name: "Public Model",
          linten_model: "linten/public",
        },
      ],
      model_name: "custom-model-name",
      linten_credential_name: "selected-credential",
      linten_extra_params: JSON.stringify({
        linten_credential_name: "from-json",
        timeout: 5,
      }),
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.lintenParamsObj.linten_credential_name).toBe("selected-credential");
    expect(deployment.lintenParamsObj.timeout).toBe(5);
  });

  it("keeps linten_credential_name from Linten Params JSON when no credential is selected", async () => {
    const formValues = {
      model_mappings: [
        {
          public_name: "Public Model",
          linten_model: "linten/public",
        },
      ],
      model_name: "custom-model-name",
      linten_extra_params: JSON.stringify({
        linten_credential_name: "from-json",
        timeout: 5,
      }),
      linten_credential_name: null,
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.lintenParamsObj.linten_credential_name).toBe("from-json");
    expect(deployment.lintenParamsObj.timeout).toBe(5);
  });

  it("saves the selected mode under model_info", async () => {
    const formValues = {
      model_mappings: [{ public_name: "Jev", linten_model: "typesafe/jev-latest" }],
      mode: "evaluation",
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.modelInfoObj.mode).toBe("evaluation");
    expect(deployment.lintenParamsObj).not.toHaveProperty("mode");
  });

  it.each([
    ["OpenAI", "openai/*"],
    ["Azure_AI_Studio", "azure_ai/*"],
    ["Petals", "petals/*"],
  ])("composes wildcard names for the all-model selection", async (custom_llm_provider, wildcardModel) => {
    const formValues = {
      model_mappings: [],
      model: "all-wildcard",
      custom_llm_provider,
    };

    const deployments = await prepareModelAddRequest({ ...formValues }, "token", null);

    expect(deployments).toHaveLength(1);
    const [deployment] = deployments!;
    expect(deployment.modelName).toBe(wildcardModel);
    expect(deployment.lintenParamsObj.model).toBe(wildcardModel);
  });
});
