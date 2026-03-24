from app.routers.pdf import GeneratePDFRequest, preflight_pdf


def test_preflight_endpoint_logic_returns_parsed_blocks():
    import asyncio

    request = GeneratePDFRequest(content="# Title\n- item", layout_id="default", title="Doc")
    response = asyncio.run(preflight_pdf(request))
    assert response.valid is True
    assert isinstance(response.blocks, list)
