from pydantic import BaseModel, ConfigDict
from datetime import date

class DeputadoOrgaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    nome_deputado: str | None
    nome: str | None          # Nome da Comissão/Orgão
    sigla: str | None
    cargo: str | None
    sigla_uf: str | None      # UF
    data_inicio: date | None
    data_final: date | None
    sigla_partido: str | None # Partido