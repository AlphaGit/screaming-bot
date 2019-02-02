#!/bin/bash
tail -n 100000 text_source.txt > text_source_truncated.txt
cp -lf text_source_truncated.txt text_source.txt
rm text_source_truncated.txt