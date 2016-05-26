title: Notes Miscellanea
css: Notes_Miscellanea.css

# Notes Miscellanea

___

## Regex

### IP Patterns

- Simple (with port): `(?'ip'\d*\.\d*\.\d*\.\d*):?(?'port'\d*)`
    - after matching, make sure that: each `ip` block is less than 256, `port` is less than 25536
- More complex (no port): `(?'ip'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$)` 
