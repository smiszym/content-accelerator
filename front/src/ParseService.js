import sanitizeHtml from "sanitize-html";
import parse from "html-react-parser";
import React from "react";

export const ParseService = {
  parse: function(content, loadPageFromUrl) {
    const sanitizedHtml = sanitizeHtml(content.text, {
      allowedTags: sanitizeHtml.defaults.allowedTags.concat(
        ['h1', 'h2', 'dl', 'dt', 'dd', 'sup'])
    });
    const elements = parse(sanitizedHtml, {
      replace: domNode => {
        if (domNode.type === "tag" && domNode.name === "a" && domNode.attribs
            && domNode.children.length === 1
            && domNode.children[0].type === "text") {
          return <a
              href={domNode.attribs.href}
              onClick={evt => {
                loadPageFromUrl(domNode.attribs.href);
                evt.preventDefault();
              }} >
            {domNode.children[0].data}
          </a>;
        } else if (domNode.type === "tag" && domNode.name === "table") {
          // Remove entire tables from the document
          return <span className="page-altered table-removed">(ukryto tabelę)</span>;
        }
      }
    });
    return elements;
  }
};