import pytest

from src.services import periodo_service


class DummyPeriodo:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.id = kwargs.get("id", 1)

    @classmethod
    async def create(cls, **kwargs):
        return DummyPeriodo(**kwargs)


@pytest.mark.asyncio
async def test_create_periodo(monkeypatch):
    monkeypatch.setattr(periodo_service, "Periodo", DummyPeriodo)
    periodo = await periodo_service.create_periodo(
        user_id=3,
        nombre="Test",
        fecha_inicio="2021-01-01",
        fecha_fin="2021-02-01",
        descripcion="desc",
    )
    assert isinstance(periodo, DummyPeriodo)
    assert periodo.usuario_id == 3
    assert periodo.nombre == "Test"


@pytest.mark.asyncio
async def test_list_periodos_by_user(monkeypatch):
    # fake return from ORM filter
    fake_list = [DummyPeriodo(id=1, usuario_id=5), DummyPeriodo(id=2, usuario_id=5)]
    class QuerySet:
        def __init__(self):
            pass
        async def order_by(self, *args, **kwargs):
            return fake_list
        async def all(self):
            return fake_list

    monkeypatch.setattr(periodo_service, "Periodo", DummyPeriodo)
    monkeypatch.setattr(DummyPeriodo, "filter", classmethod(lambda cls, **kwargs: QuerySet()))
    result = await periodo_service.list_periodos_by_user(5)
    assert isinstance(result, list)
    assert result[0]["usuario_id"] == 5
