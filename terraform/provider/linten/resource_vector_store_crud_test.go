package linten

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
	"github.com/hashicorp/terraform-plugin-sdk/v2/terraform"
)

func TestVectorStoreReadDoesNotPersistServerLintenParams(t *testing.T) {
	resp := VectorStoreResponse{
		VectorStoreID:     "vs-123",
		VectorStoreName:   "kb",
		CustomLLMProvider: "openai",
		LintenParams: map[string]interface{}{
			"api_key":  "sk-from-server",
			"api_base": "https://upstream.example.com",
		},
	}
	body, _ := json.Marshal(resp)

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write(body)
	}))
	defer srv.Close()

	client := NewClient(srv.URL, "test-key", true)
	d := schema.TestResourceDataRaw(t, resourceLintenVectorStore().Schema, map[string]interface{}{
		"vector_store_name":   "kb",
		"custom_llm_provider": "openai",
		"linten_params": map[string]interface{}{
			"vector_store_id": "vs-123",
		},
	})
	d.SetId("vs-123")

	if err := resourceLintenVectorStoreRead(d, client); err != nil {
		t.Fatalf("read failed: %v", err)
	}

	got := d.Get("linten_params").(map[string]interface{})
	if _, leaked := got["api_key"]; leaked {
		t.Fatalf("server-returned api_key persisted into state: %v", got)
	}
	if got["vector_store_id"] != "vs-123" {
		t.Fatalf("config linten_params not preserved: %v", got)
	}
	if d.Get("vector_store_name").(string) != "kb" {
		t.Fatalf("read did not populate non-sensitive fields")
	}
}

func TestVectorStoreLintenParamsWarnsOnSecretKeys(t *testing.T) {
	diags := resourceLintenVectorStore().Validate(terraform.NewResourceConfigRaw(map[string]interface{}{
		"vector_store_name":   "kb",
		"custom_llm_provider": "openai",
		"linten_params": map[string]interface{}{
			"api_key":         "sk-in-state",
			"vector_store_id": "vs-123",
		},
	}))
	if diags.HasError() {
		t.Fatalf("a secret key must warn, not fail: %v", diags)
	}
	var warned []string
	for _, d := range diags {
		if d.Severity == diag.Warning {
			warned = append(warned, d.Summary)
		}
	}
	if len(warned) != 1 || !strings.Contains(warned[0], `"api_key"`) {
		t.Fatalf("expected exactly one warning naming api_key, got %v", warned)
	}

	clean := resourceLintenVectorStore().Validate(terraform.NewResourceConfigRaw(map[string]interface{}{
		"vector_store_name":   "kb",
		"custom_llm_provider": "openai",
		"linten_params":      map[string]interface{}{"vector_store_id": "vs-123"},
	}))
	if len(clean) != 0 {
		t.Fatalf("non-secret keys must not warn, got %v", clean)
	}
}
