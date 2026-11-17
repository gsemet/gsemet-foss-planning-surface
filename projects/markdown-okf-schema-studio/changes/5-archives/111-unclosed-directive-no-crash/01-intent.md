When a document contain the opening of a list-table but not the close

````md

```{list-table}

````

it crashs instead of just printing the raw line

---

Same with this

````md

(label-name

:::{table} Caption

:::

)=
````

more generally, syntax error should be much better tested !
