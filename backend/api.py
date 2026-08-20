from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

# Inicialização da API REST desenvolvida em Python/FastAPI
app = FastAPI(
    title="Concilia IA API",
    description=(
        "API para apoiar conciliadores do CEJUSC/TJMS na análise de processos "
        "de saúde suplementar, utilizando inteligência artificial, regras da ANS "
        "e validação humana (human-in-the-loop)."
    ),
    version="1.0.0",
)


# Modelos Pydantic para validação de dados
class ProcessoSaudeRequest(BaseModel):
    numero_processo: str
    detalhes_peticao: str
    documentos_s3_url: Optional[str] = None  # Integração com Object Storage (S3)


class AnaliseResponse(BaseModel):
    numero_processo: str
    parecer_ia: str
    regras_ans_aplicadas: List[str]
    status_validacao: str  # Suporta o fluxo de human-in-the-loop


class ValidacaoHumanaRequest(BaseModel):
    aprovado: bool
    observacoes_conciliador: str


@app.get("/health", tags=["Operação"])
def verificar_saude():
    """Indica que o serviço está disponível para receber requisições."""
    return {"status": "ok"}


# --- Autenticação e Segurança ---
@app.post("/api/v1/auth/token", tags=["Segurança e Autenticação"])
def gerar_token_jwt():
    """
    Endpoint de configurações de segurança e autenticação via JWT[cite: 1].
    """
    # Implementação padrão de emissão de token de acesso
    return {"access_token": "token_jwt_exemplo_gerado", "token_type": "bearer"}


# --- Módulo de Análise com Inteligência Artificial e RAG ---
@app.post(
    "/api/v1/processos/analisar",
    response_model=AnaliseResponse,
    tags=["Análise de Processos"],
)
def analisar_processo_saude(processo: ProcessoSaudeRequest):
    """
    Realiza a análise do processo de saúde utilizando:
    - Prompts e parâmetros integrados aos modelos de IA (OpenAI / Claude) via gateway[cite: 1].
    - Bases de dados normativas (Rol da ANS, Diretrizes de Utilização e resoluções)[cite: 1].
    - Busca semântica (RAG) utilizando PostgreSQL com extensão pgvector[cite: 1].
    """

    # Exemplo simulado da resposta gerada pela IA e regras da ANS
    return AnaliseResponse(
        numero_processo=processo.numero_processo,
        parecer_ia=(
            "Parecer gerado via modelo de IA integrado: O procedimento solicitado "
            "encontra respaldo nas normativas vigentes da ANS."
        ),
        regras_ans_aplicadas=[
            "Rol da ANS - Cobertura Obrigatória",
            "Diretrizes de Utilização (DUT)",
        ],
        status_validacao="Pendente de Validação Humana",
    )


# --- Módulo de Validação Humana (Human-in-the-Loop) ---
@app.post("/api/v1/processos/{numero_processo}/validar", tags=["Validação Humana"])
def registrar_validacao_humana(numero_processo: str, validacao: ValidacaoHumanaRequest):
    """
    Etapa de validação humana (human-in-the-loop) realizada pelos conciliadores do CEJUSC/TJMS[cite: 1].
    """
    status_final = (
        "Aprovado pelo Conciliador"
        if validacao.aprovado
        else "Rejeitado/Revisão Necessária"
    )

    return {
        "numero_processo": numero_processo,
        "status_atual": status_final,
        "observacoes": validacao.observacoes_conciliador,
        "mensagem": "Validação registrada com sucesso no sistema.",
    }
