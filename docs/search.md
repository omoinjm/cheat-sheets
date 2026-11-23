---
layout: default
title: Search
permalink: /search/
---

<!-- Tailwind CSS CDN -->
<script src="https://cdn.tailwindcss.com"></script>

<div class="max-w-4xl mx-auto p-6 bg-gray-900 text-white min-h-screen">
  <h1 class="text-3xl font-bold mb-6 text-blue-400">Knowledge Base Search</h1>
  
  <input type="text" id="search-box"
    class="w-full p-4 border-2 border-gray-700 rounded-lg mb-6 bg-gray-800 text-white focus:outline-none focus:border-blue-500 transition-colors"
    placeholder="Search the knowledge base...">

  <div id="status" class="text-gray-400 mb-4 italic">Loading index...</div>

  <ul id="search-results" class="space-y-4"></ul>
</div>

<script>
  const resultsList = document.getElementById("search-results");
  const searchBox = document.getElementById("search-box");
  const statusIndicator = document.getElementById("status");
  let indexedDocs = [];

  // Step 4: Load and Search (Adapted for Jekyll JSON index)
  async function loadDocs() {
    try {
      const res = await fetch('{{ site.baseurl }}/search.json');
      indexedDocs = await res.json();
      statusIndicator.textContent = `${indexedDocs.length} pages indexed. Ready to search.`;
      
      // Focus search box
      searchBox.focus();
    } catch (error) {
      console.error("Failed to load search index:", error);
      statusIndicator.textContent = "Error loading search index.";
    }
  }

  function searchDocs(term) {
    resultsList.innerHTML = "";
    if (!term || term.length < 2) {
      return;
    }

    const lowerTerm = term.toLowerCase();
    
    // Simple filter logic from the article
    const results = indexedDocs.filter(doc =>
      doc.title.toLowerCase().includes(lowerTerm) || 
      doc.content.includes(lowerTerm)
    );

    if (results.length === 0) {
      resultsList.innerHTML = '<li class="text-gray-500">No matching articles found.</li>';
      return;
    }

    results.forEach(result => {
      const li = document.createElement("li");
      li.className = "transform transition-all duration-200 hover:translate-x-2";
      li.innerHTML = `
        <a href="${result.url}" class="block p-4 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700 hover:border-blue-500 group">
          <div class="text-xl font-semibold text-blue-400 group-hover:text-blue-300">${result.title}</div>
          <div class="text-sm text-gray-400 mt-1">${result.url}</div>
        </a>
      `;
      resultsList.appendChild(li);
    });
  }

  searchBox.addEventListener("input", (e) => {
    searchDocs(e.target.value);
  });

  // Start loading
  loadDocs();
</script>

<style>
  /* Ensure Tailwind doesn't conflict too much with Hacker theme basics */
  #main_content { max-width: none !important; }
</style>
