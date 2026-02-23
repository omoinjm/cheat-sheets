---
title: Understanding Struct Size and Memory Alignment in C
description: A detailed explanation of C struct size, memory alignment, padding, and the impact of packing directives.
type: content
path: development/languages/c & c++/structs.md
tags: [development, languages, c, c++, memory-management, structs]
---
# Understanding Struct Size and Memory Alignment in C

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../../README.md)

## Parent Context

This document is part of the C & C++ programming language notes, focusing on fundamental memory management concepts.

## Contents Overview

This file provides a detailed explanation of how C structures are sized in memory, covering memory alignment, padding rules, and the use of directives like `#pragma pack` and `__attribute__((packed))` to control these behaviors. It also discusses the implications of such controls on performance and portability.

## Role in System

This document is crucial for C/C++ developers who need to understand and optimize low-level memory usage, especially in performance-critical applications, embedded systems development, or when dealing with binary data serialization and hardware interfaces. A solid grasp of these concepts helps in writing efficient and bug-free code.

## Key Concepts

### 1. How Big is the Struct?

Explains how `sizeof` a struct is affected by `char` and `int` sizes and compiler-added padding to ensure memory alignment, typically resulting in a size larger than the sum of its members.

### 2. How Does a 64-bit System Affect the Struct Size?

Clarifies that struct size and alignment rules generally remain consistent across 32-bit and 64-bit systems for basic types, with 64-bit systems primarily affecting pointer sizes.

### 3. When is it Appropriate to Force the Struct to be 5 Bytes?

Details the use of `#pragma pack(1)` or `__attribute__((packed))` to disable padding, forcing a struct to its minimum possible size. It outlines appropriate scenarios (binary data serialization, hardware interfacing, reducing memory in large arrays) and warns against inappropriate use (performance degradation due to unaligned access, portability issues).

### Size vs. Performance Trade-Off

A table illustrating the trade-offs between a packed struct (smaller memory, slower performance) and a default-aligned struct (larger memory, faster performance, better portability).

## Final Recommendation

Provides guidance on when to prioritize strict memory constraints (use `#pragma pack`) versus performance (allow compiler to add padding).
