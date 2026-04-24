from pydantic import BaseModel, ConfigDict
from datetime import date

class DeputadoOrgaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    nome_deputado: str | None
    nome: str | None               # Nome do Órgão (ex: Comissão de Educação)
    sigla: str | None              # Sigla do Órgão
    cargo: str | None              # Cargo que o deputado ocupa lá
    sigla_uf: str | None           # Estado (UF) do deputado
    data_inicio: date | None
    data_final: date | None
    sigla_partido: str | None      # Partido do deputado