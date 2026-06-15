<script>
  import Router from 'svelte-spa-router'
  import Navbar from './components/Navbar.svelte'
  import Footer from './components/Footer.svelte'
  import Home from './pages/Home.svelte'
  import Buildings from './pages/Buildings.svelte'
  import BuildingDetail from './pages/BuildingDetail.svelte'
  import MapView from './pages/MapView.svelte'
  import Rankings from './pages/Rankings.svelte'
  import Login from './pages/Login.svelte'
  import Register from './pages/Register.svelte'
  import Upload from './pages/Upload.svelte'
  import RoutesPage from './pages/Routes.svelte'
  import { auth } from './stores/auth'

  const routes = {
    '/': Home,
    '/buildings': Buildings,
    '/buildings/:id': BuildingDetail,
    '/map': MapView,
    '/rankings': Rankings,
    '/routes': RoutesPage,
    '/login': Login,
    '/register': Register,
    '/upload': Upload
  }
</script>

<div class="app-wrapper">
  <Navbar />

  <main class="main-content">
    <Router {routes} />
  </main>

  <Footer />
</div>

<style>
  .app-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .main-content {
    flex: 1;
    padding-top: 70px;
  }
</style>
