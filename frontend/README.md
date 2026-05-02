# Frontend Scaffold

Frontend ini disiapkan dengan:

- React
- React Router
- React Query
- Axios
- Ant Design
- Vite

## Struktur Utama

- `src/app/`: layout aplikasi, router, provider, dan shared UI global
- `src/features/`: area fitur per domain seperti dashboard, dataset, training, prediction
- `src/lib/`: API client, react-query, hooks, types, utils
- `src/styles/`: CSS global

Struktur ini sekarang mengikuti pola yang lebih dekat ke referensi belajar:

- `app/layout`
- `app/router`
- `app/shared`
- `features/...`
- `lib/...`

## Menjalankan

```bash
npm install
npm run dev
```

Sebelum menjalankan, copy `.env.example` menjadi `.env` jika ingin mengganti base URL API.
