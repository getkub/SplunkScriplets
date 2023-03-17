## Use for_each instead of index.loop
```
dynamic "allow" {
    for_each = each.value.action == "allow" ? [{
        ports = each.value.ports
    }]: []

    content {
        protocol = allow.value["ports"]
    }
}

my_tags = each.value.my_tags
cidr_ranges_src = each.value.flow == "EGRESS" ? each.value.cidr_ranges_src: null
other_optional_field = try(each.value.flow == "EGRESS" ? each.value.other_optional_field: null , null)

```