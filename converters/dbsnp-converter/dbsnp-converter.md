# dbSNP Converter

Takes lists of rsIDs as input. Format as follows.

```
#rsid   sample_id   tag
rs113993959 s01 cystic_fibrosis
...
```
The `sample_id` and `tag` columns are optional and may be omitted. The first line must begin with `#rsid`. Subsequent lines may use `#` to add a comment. Separate columns with tabs or one or more spaces.