from app.services.markdown_parser import MarkdownParser


def test_parser_drops_blank_list_items_and_keeps_valid_ones():
    parser = MarkdownParser()
    parsed = parser.parse("- \n- item one\n-   \n")
    list_blocks = [b for b in parsed["blocks"] if b.get("type") == "list"]
    assert len(list_blocks) == 1
    assert list_blocks[0]["items"] == ["item one"]


def test_parser_removes_unsafe_links_and_keeps_safe_links():
    parser = MarkdownParser()
    parsed = parser.parse("[ok](https://example.com) [bad](example.com)")
    paragraph = next(b for b in parsed["blocks"] if b.get("type") == "paragraph")
    assert 'href="https://example.com"' in paragraph["text"]
    assert 'href="example.com"' not in paragraph["text"]
