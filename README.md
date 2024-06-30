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

<iframe title="dashboard" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiNjNhYTBhOTktMDE0YS00Yzg3LTg1ZDctN2JkZjIxNzJiYmE4IiwidCI6ImQ2NDZkM2E4LTdiMTUtNGI1My05ZDkyLTk4MTVmZDYyNzAyYyIsImMiOjR9" frameborder="0" allowFullScreen="true"></iframe>
