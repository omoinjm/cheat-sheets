---
layout: default
title: Search
permalink: /search/
---

<div class="search-page">
  <h1>Search Wiki</h1>
  <div id="search-container">
    <input type="text" id="search-input" placeholder="Type to search..." autofocus style="width: 100%; padding: 12px; font-size: 1.2em; border: 2px solid #444; border-radius: 6px; margin-bottom: 20px; background: #222; color: #fff;">
    <ul id="results-container" style="list-style: none; padding: 0; margin-top: 10px;"></ul>
  </div>
</div>

<style>
  #results-container li {
    margin-bottom: 12px;
    border-bottom: 1px solid #333;
    padding-bottom: 8px;
  }
  #results-container a {
    text-decoration: none;
    font-weight: bold;
    font-size: 1.2em;
    color: #4183C4;
  }
  #results-container a:hover {
    text-decoration: underline;
  }
</style>


<!-- Script to handle search -->
<script src="https://cdn.jsdelivr.net/npm/simple-jekyll-search@1.10.0/dest/simple-jekyll-search.min.js"></script>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    SimpleJekyllSearch({
      searchInput: document.getElementById('search-input'),
      resultsContainer: document.getElementById('results-container'),
      json: '{{ site.baseurl }}/search.json',
      searchResultTemplate: '<li><a href="{url}">{title}</a></li>',
      noResultsText: 'No results found',
      limit: 20,
      fuzzy: false
    });
  });
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
