# Frontend Scaffold

Frontend ini disiapkan dengan:

- React
- React Router
- React Query
- Axios
- Ant Design
- Vite

## Struktur Utama

- `src/app/`: provider global
- `src/layouts/`: layout shell aplikasi
- `src/router/`: definisi route
- `src/pages/`: halaman utama
- `src/features/`: area fitur per domain
- `src/components/`: komponen reusable
- `src/lib/`: utilitas global seperti axios dan query client
- `src/styles/`: CSS global

## Menjalankan

```bash
npm install
npm run dev
```

Sebelum menjalankan, copy `.env.example` menjadi `.env` jika ingin mengganti base URL API.
