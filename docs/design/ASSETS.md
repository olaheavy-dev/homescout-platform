# Image and asset register

Every image, map tile, font or other media file in this repository is listed here with where it came from, the terms it is used under and any attribution it needs (doc 04 §3, rule 9). Add an entry **before** a new asset is committed.

## Concept images (docs/design)

| File | What it is | Source / how made | Terms and attribution | Status |
|---|---|---|---|---|
| `HomeScout Copilot Property Intelligence-1.png` | Homepage concept | AI-generated concept image. Embedded C2PA content credentials mark it as generated; the review reported OpenAI image generation. | Governed by the generating service's terms of use; no third-party attribution recorded. **Creator to confirm** | Concept only |
| `HomeScout Property Intelligence Dashboard-2.png` | Property passport concept | As above | As above. Depicts imitation logos of HM Land Registry, GOV.UK, Environment Agency, Ofcom, DfT, Department for Education and Ordnance Survey | Concept only. Logos must not be reused |
| `HomeScout Property Intelligence Dashboard-3.png` | Copilot investigation concept | As above | As above | Concept only |
| `HomeScout Neighborhood Dashboard-4.png` | Neighbourhood concept | As above | As above. The map is a generated image, not OpenStreetMap or other map data, though its data note names OpenStreetMap | Concept only |
| `HomeScout Property Comparison Dashboard-5.png` | Comparison concept | As above | As above | Concept only. Figures are wrong (doc 03 §2) |
| `HomeScout Lease Review Dashboard-6.png` | Document review concept | As above | As above. The lease text is generated, not a real lease | Concept only |
| `HomeScout Property Dashboard-7.png` | Workspace concept | As above | As above | Concept only |
| `HomeScout Property Insights Dashboard-8.png` | Alternative workspace concept | As above | As above | Concept only |
| `abode_copilot.jpeg` | Contact sheet of images 1–6 and 8 | No embedded provenance metadata. Assumed to be assembled from the images above. **Creator to confirm** | As above | Concept only |

## Rules for these images

- They are **design concepts for discussion**, not product assets. They must not be used in the prototype, the product or marketing.
- Their depictions of official bodies' logos, maps, addresses, prices and documents are generated imitations, not real data or endorsements. Doc 03 §2 and §7 already require that none of this carries into the product.
- The all-rights-reserved notice in `LICENSE` covers the project's own work. It doesn't claim rights in third-party names or marks depicted in the images.
- If the generating service's terms or the creator's confirmation turns out to conflict with publishing them, remove the images from the repository.

## Product assets

None yet. The image pass in stage 4 (doc 03 §7) adds entries here before any file is committed.
