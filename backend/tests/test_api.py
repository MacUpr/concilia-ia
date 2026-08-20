from backend.api import (
    ProcessoSaudeRequest,
    ValidacaoHumanaRequest,
    analisar_processo_saude,
    app,
    registrar_validacao_humana,
    verificar_saude,
)


def test_health_check_and_routes():
    assert verificar_saude() == {"status": "ok"}

    paths = app.openapi()["paths"]
    assert "/health" in paths
    assert "/api/v1/processos/analisar" in paths
    assert "/api/v1/processos/{numero_processo}/validar" in paths


def test_analisar_processo():
    response = analisar_processo_saude(
        ProcessoSaudeRequest(
            numero_processo="0001234-56.2026.8.12.0001",
            detalhes_peticao="Pedido de cobertura para procedimento médico.",
        )
    )

    assert response.numero_processo == "0001234-56.2026.8.12.0001"
    assert response.status_validacao == "Pendente de Validação Humana"


def test_registrar_validacao_humana():
    response = registrar_validacao_humana(
        "0001234-56.2026.8.12.0001",
        ValidacaoHumanaRequest(aprovado=True, observacoes_conciliador="Validado."),
    )

    assert response["status_atual"] == "Aprovado pelo Conciliador"
