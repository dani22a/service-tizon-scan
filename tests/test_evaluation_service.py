import pytest

from src.services import evaluation_service


@pytest.mark.asyncio
async def test_create_prediccion_fase1_includes_periodo(monkeypatch):
    captured = {}

    class FakePred:
        def __init__(self):
            self.id = 123
            self.surco_id = None
            self.usuario_id = None
            self.periodo_id = None
            self.imagen_url = None
            self.fase1_resumen = None
            self.fase1_payload = None
            self.fase2_resumen = None
            self.fase2_payload = None
            self.fecha = None
            self.created_at = None
            self.updated_at = None

        @classmethod
        async def create(cls, **kwargs):
            captured.update(kwargs)
            return FakePred()

    monkeypatch.setattr(evaluation_service, "Prediccion", FakePred)

    # call with period id
    await evaluation_service.create_prediccion_fase1(
        user_id=7,
        imagen_url="http://example.com/img.jpg",
        fase1_payload={"foo": "bar"},
        surco_id=2,
        periodo_id=5,
    )

    assert captured.get("periodo_id") == 5
    assert captured.get("usuario_id") == 7
    assert captured.get("surco_id") == 2


def test_prediccion_to_dict_includes_periodo():
    class P:
        def __init__(self):
            self.id = 9
            self.surco_id = None
            self.usuario_id = None
            self.periodo_id = 42
            self.imagen_url = "url"
            self.fase1_resumen = {}
            self.fase1_payload = {}
            self.fase2_resumen = {}
            self.fase2_payload = {}
            self.fecha = None
            self.created_at = None
            self.updated_at = None

    p = P()
    d = await evaluation_service.prediccion_to_dict(p)
    assert d["periodo_id"] == 42
