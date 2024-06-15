# Electro-pricing
Generador de estrategia de pricing. A través de web scraping de 30 empresas top del mercado se recopila información. Esta se almacena en postgres para luego visualizar en Power Bi. Finalmente, se identifica la estrategia con regresión lineal entre variables explicativas de un precio competitivo. 

Este proyecto tiene la siguiente estructura:

```
└── 📁c18-58-ft-data-bi
    └── .gitignore
    └── LICENSE
    └── README.md
    └── 📁src
        └── 📁data-pipelines
        └── 📁visualizations
        ├── 📁web-scrapy
```

Donde los scripts se ejecutaran a partir de la carpeta src.
