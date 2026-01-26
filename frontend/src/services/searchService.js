// src/services/searchService.js

// Base fake de dados
const fakeData = [
  { id: 1, name: "Notebook Gamer", description: "Notebook potente para jogos", category: "electronics" },
  { id: 2, name: "Monitor 27\"", description: "Monitor Full HD", category: "electronics" },
  { id: 3, name: "Teclado Mecânico", description: "Teclado RGB", category: "electronics" },
  { id: 4, name: "Consultoria Empresarial", description: "Serviços de consultoria", category: "services" },
  { id: 5, name: "Sistema ERP", description: "ERP para empresas", category: "software" },
]

// Simula delay de API
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export const search = async (q, category = "all") => {
  await delay(300)

  const query = (q || "").toLowerCase()

  let results = fakeData.filter((item) =>
    item.name.toLowerCase().includes(query)
  )

  if (category !== "all") {
    results = results.filter((item) => item.category === category)
  }

  return results
}

// Retorna só sugestões (autocomplete)
export const suggest = async (q) => {
  await delay(150)

  const query = (q || "").toLowerCase()

  if (!query) return []

  return fakeData
    .filter((item) => item.name.toLowerCase().includes(query))
    .slice(0, 5)
}
