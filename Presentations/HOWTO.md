# Introduction
Presentations are written in Markdown and rendered in the browser by [remark](http://remarkjs.com). 

## Getting started
To create a new presentation:
1. Create a new directory under GE-Gravy/Presentations
2. Create a new Markdown file containing the presentation content.
3. Create a new HTML file based on [TEMPLATE](https://github.com/USITC/GE-Gravity/edit/master/Presentations/TEMPLATE) in the new directory.
4. Modify the HTML file to:
    - Provide a page title in the `<title>` tag.
    - Provide the link to the Markdown file in the `sourceUrl` property within the `<script>` tag.
    - Modify the presentation styling as needed.
5. Modify the main [README](https://github.com/USITC/GE-Gravity/edit/master/Presentations/README.md) file with:
    - A link to the slideshow (development version).
    - A few bullet points describing the content.
