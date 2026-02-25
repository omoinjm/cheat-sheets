---
layout: page
title: Search
permalink: /search/
---

<div id="search-container">
  <input type="text" id="search-input" placeholder="Search wiki..." autofocus style="width: 100%; padding: 10px; margin-bottom: 20px; color: #333;">
  <ul id="results-container"></ul>
</div>

<!-- Script to handle search -->
<script src="https://unpkg.com/simple-jekyll-search@latest/dest/simple-jekyll-search.min.js"></script>

<script>
  window.simpleJekyllSearch = SimpleJekyllSearch({
    searchInput: document.getElementById('search-input'),
    resultsContainer: document.getElementById('results-container'),
    json: '{{ "/search.json" | relative_url }}',
    searchResultTemplate: '<li><a href="{url}">{title}</a></li>',
    noResultsText: 'No results found',
    limit: 10,
    fuzzy: false,
    exclude: ['Welcome']
  })
</script>

<style>
  #search-input {
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    background-color: white;
  }
  #results-container {
    list-style: none;
    padding-left: 0;
  }
  #results-container li {
    margin-bottom: 10px;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
  }
  #results-container a {
    text-decoration: none;
    font-weight: bold;
    font-size: 1.1em;
  }
</style>
