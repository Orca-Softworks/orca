galaxy_definition = layer_definition(
    query_parts = [
        "name": string_query(),
        "type": variant_query(
            ["variant_one", "variant_two", "variant_3"]
        )
    ]
)

system_definition = layer_definition(
    query_language = ""
)

star_definition = layer_definition()

system_definition = layer_definition()

planet_definition = layer_definition()
computer_definition = layer_definition()

# actually this is the base layer. base layer can be recursive.
machine_definition = layer_definition(
    query_parts = [
        "name": string_query(),
    ],
    recursive = True,
)

# so you define your own hierarchy of layers in a system, each with a query
# to help describe how you should attempt to find the instance within the
# hierarchy

# example string query and what it means
# AND, OR, NOT is a functionally complete set, should work for describing queries
#
# "name[nice].or[name[okay]].or[name[yes]]" any of nice, okay, or yes
# "name[cool].and[type[variant_one]]" qualify one part of a query with and additional part of the query
# "[name[nice].or[name[okay]]].and[not[type[variant_two]]]" the name can be nice or okay, but type cannot be variant_two
# [name[regex[[0-9]]]] we can also use regex for strings, and we will match those that match the regex