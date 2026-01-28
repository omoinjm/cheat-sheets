---
type: directory
path: languages/c & c++
parent: languages
tags: [repo, documentation, languages, c, c++, programming]
---
# C & C++ Programming Language Notes

## 🔗 Navigation
- [[../README|⬆ Parent]]
- [[../../../README|🏠 Root]]
- [[./|📂 Current Directory]]

## 📌 Overview
This directory contains notes and detailed explanations of core concepts in C and C++ programming, with a specific focus on memory management and data structures. It provides foundational knowledge for writing efficient and correct C/C++ code.

<h2> 📁 Contents</h2>
- [[structs.md]]: A detailed explanation of C struct size, memory alignment, padding, and the impact of packing directives.
- [[README.md]]: This file, providing an overview of C & C++ programming notes.

<h2> 🧠 Responsibilities</h2>
This section is vital for understanding low-level memory management and optimization in C and C++, which is critical for system programming, embedded systems, and performance-sensitive applications.

<h2> 🔄 Relationships</h2>
This directory is a child of the [[../README|languages]] directory. Concepts detailed here, particularly regarding memory management, are fundamental for understanding [[../../../pen-testing/reserve-engineering/README|reverse engineering]] and optimizing performance in various [[../../../os/README|operating system]] contexts.

<h2> 💡 Featured Topic: Understanding Struct Size and Memory Alignment in C</h2>
The `structs.md` document delves into the intricacies of how C compilers manage memory for `struct` types.

### Key Concepts Covered:

-   **Memory Layout**: Explains how `char` and `int` members are laid out in memory, including the role of padding bytes for alignment.
-   **`sizeof` Operator**: Demonstrates how to programmatically check the size of a `struct`.
-   **64-bit System Impact**: Clarifies that while pointers change size, basic types like `int` and `char` generally retain their sizes, and alignment rules remain consistent.
-   **Forcing Struct Packing**: Discusses the use of `#pragma pack(1)` or `__attribute__((packed))` to disable padding and achieve a compact memory layout.
-   **Trade-offs**: Outlines the appropriate scenarios for using forced packing (e.g., binary serialization, hardware interfacing) versus when to avoid it due to performance implications (slower unaligned access) and portability issues. A table summarizes the trade-offs between packed and default alignment.

This document emphasizes the importance of understanding these low-level details for writing efficient, portable, and correct C/C++ code, especially when dealing with specific memory constraints or external data formats.