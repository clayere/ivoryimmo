// ============================================================
// IVORY IMMO — Shared Properties Data
// ============================================================

const PROPERTIES = [
  {
    id: 1,
    title: "Appartement Luxe Cocody",
    type: "appartement",
    location: "Cocody, Abidjan",
    image: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=700",
    features: { "Surface": "120 m²", "Pièces": "4 pièces", "Étage": "3ème étage", "Parking": "1 place" },
    description: "Magnifique appartement lumineux en plein cœur de Cocody. Vue dégagée, cuisine entièrement équipée, grand balcon. Résidence sécurisée avec gardien 24h/24 et générateur électrique.",
    prix_location: "350 000 FCFA/mois",
    prix_vente: "65 000 000 FCFA",
    modes: ["location", "vente"]
  },
  {
    id: 2,
    title: "Studio Moderne Plateau",
    type: "studio",
    location: "Le Plateau, Abidjan",
    image: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=700",
    features: { "Surface": "35 m²", "Pièces": "1 pièce", "Étage": "2ème étage", "Parking": "Non inclus" },
    description: "Studio entièrement rénové avec des matériaux de qualité, idéal pour jeune professionnel. Proche de toutes commodités, transports, commerces. Connexion fibre optique incluse.",
    prix_location: "120 000 FCFA/mois",
    prix_vente: "15 000 000 FCFA",
    modes: ["location", "vente"]
  },
  {
    id: 3,
    title: "Villa Prestige Riviera",
    type: "villa",
    location: "Riviera Golf, Abidjan",
    image: "https://images.unsplash.com/photo-1416331108676-a22ccb276e35?w=700",
    features: { "Surface": "450 m²", "Pièces": "6 pièces", "Étage": "R+1", "Parking": "3 places" },
    description: "Villa d'exception avec piscine privée, jardin tropical entretenu, salle de sport équipée. Domaine entièrement clôturé, vidéosurveillance 24h/24. Finitions haut de gamme importées.",
    prix_location: "1 500 000 FCFA/mois",
    prix_vente: "350 000 000 FCFA",
    modes: ["location", "vente"]
  },
  {
    id: 4,
    title: "Appartement Vue Mer Bassam",
    type: "appartement",
    location: "Grand-Bassam",
    image: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=700",
    features: { "Surface": "80 m²", "Pièces": "3 pièces", "Étage": "4ème étage", "Parking": "1 place" },
    description: "Appartement avec vue imprenable sur l'océan Atlantique. Grande terrasse privatisée, résidence avec sécurité. Idéal pour résidence principale, secondaire ou investissement locatif.",
    prix_location: "280 000 FCFA/mois",
    prix_vente: "45 000 000 FCFA",
    modes: ["location", "vente"]
  },
  {
    id: 5,
    title: "Studio Étudiant Deux-Plateaux",
    type: "studio",
    location: "Deux-Plateaux, Abidjan",
    image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=700",
    features: { "Surface": "28 m²", "Pièces": "1 pièce", "Étage": "1er étage", "Parking": "Non inclus" },
    description: "Studio fonctionnel proche des universités et grandes écoles. Cuisine équipée, climatisation, connexion internet haut débit. Parfait pour étudiant ou jeune actif souhaitant se loger à Abidjan.",
    prix_location: "80 000 FCFA/mois",
    prix_vente: null,
    modes: ["location"]
  },
  {
    id: 6,
    title: "Villa Contemporaine Angré",
    type: "villa",
    location: "Angré, Abidjan",
    image: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=700",
    features: { "Surface": "320 m²", "Pièces": "5 pièces", "Étage": "R+1", "Parking": "2 places" },
    description: "Villa de style contemporain avec matériaux nobles et architecture soignée. Grand salon baigné de lumière, cuisine américaine ouverte sur terrasse, chambres avec dressings intégrés.",
    prix_location: null,
    prix_vente: "180 000 000 FCFA",
    modes: ["vente"]
  },
  {
    id: 7,
    title: "Appartement T3 Marcory",
    type: "appartement",
    location: "Marcory, Abidjan",
    image: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=700",
    features: { "Surface": "65 m²", "Pièces": "3 pièces", "Étage": "2ème étage", "Parking": "1 place" },
    description: "Appartement T3 bien situé dans le quartier résidentiel de Marcory. Accès rapide aux axes principaux, proche commerces et écoles. Logement en excellent état général.",
    prix_location: "200 000 FCFA/mois",
    prix_vente: "28 000 000 FCFA",
    modes: ["location", "vente"]
  },
  {
    id: 8,
    title: "Villa Piscine Bingerville",
    type: "villa",
    location: "Bingerville",
    image: "https://images.unsplash.com/photo-1613977257365-aaae5a9817ff?w=700",
    features: { "Surface": "500 m²", "Pièces": "7 pièces", "Étage": "R+1", "Parking": "4 places" },
    description: "Villa hors norme nichée dans la verdure de Bingerville. Piscine à débordement avec vue sur la lagune, court de tennis, maison de gardien indépendante. Un véritable havre de paix.",
    prix_location: null,
    prix_vente: "500 000 000 FCFA",
    modes: ["vente"]
  },
  {
    id: 9,
    title: "Studio Neuf Yopougon",
    type: "studio",
    location: "Yopougon, Abidjan",
    image: "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=700",
    features: { "Surface": "32 m²", "Pièces": "1 pièce", "Étage": "RC", "Parking": "Non inclus" },
    description: "Studio flambant neuf dans une résidence moderne de Yopougon. Finitions soignées, climatisation split, chauffe-eau solaire. Idéal pour premier logement ou investissement.",
    prix_location: "95 000 FCFA/mois",
    prix_vente: "12 000 000 FCFA",
    modes: ["location", "vente"]
  }
];

// Count by type
function countByType(type) {
  return PROPERTIES.filter(p => p.type === type).length;
}
