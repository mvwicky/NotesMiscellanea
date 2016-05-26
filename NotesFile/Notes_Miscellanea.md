title: Notes Miscellanea
css: Notes_Miscellanea.css

# Notes Miscellanea

___

## Regex

### Patterns

- Simple IP (with port): `(?'ip'\d*\.\d*\.\d*\.\d*):?(?'port'\d*)`
    - after matching, make sure that: each `ip` block is less than 256, `port` is less than 25536
- More complex IP (no port): `(?'ip'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$)` 
- Date: `(?'date'^(\d{1,4})-(1[0-2]|0?[1-9])-(3[0-1]|[1-2][0-9]|0?[1-9])$)`
- Time: `(?'time'^(2[0-3]|1[0-9]|0?[0-9]):([1-5][0-9]|0?[0-9])$)`
