<template>
    <main>
        <ECard>
            <!--
            <h1 class="align-center text-center text-3xl font-bold">
                Bienvenido
            </h1>

            <div class="flex gap-3">
                <EButton>Test primary Button</EButton>
                <EButton type="secondary">Test secondary
                    Button</EButton>
            </div>
             -->
        </ECard>

        <div class="container" style="background-color: white; border-radius: 5px">
            <div class="container" style="background-color: white; padding: 10px">
                <h1 style="font-size: 35px; color: black">Bodega 1</h1>
            </div>

            <!--GRUPO DE BOTONES-->
            <div
                class="btn-group"
                role="group"
                aria-label="Basic radio toggle button group"
                style="padding: 10px">
                <input
                    type="radio"
                    class="btn-check"
                    name="btnradio"
                    id="btnradio1"
                    autocomplete="off"
                    checked />
                <label class="btn btn-outline-dark" for="btnradio1"
                    >Inventario</label
                >

                <input
                    type="radio"
                    class="btn-check"
                    name="btnradio"
                    id="btnradio2"
                    autocomplete="off" />
                <label class="btn btn-outline-dark" for="btnradio2"
                    >Historia Pedidos</label
                >

                <input
                    type="radio"
                    class="btn-check"
                    name="btnradio"
                    id="btnradio3"
                    autocomplete="off" />
                <label class="btn btn-outline-dark" for="btnradio3"
                    >Tomas Fisicas</label
                >

                <input
                    type="radio"
                    class="btn-check"
                    name="btnradio"
                    id="btnradio3"
                    autocomplete="off" />
                <label class="btn btn-outline-dark" for="btnradio3"
                    >Movimientos</label
                >
            </div>

            <!--DIV DE BOTONES Y NAV-->
            <div class="container text-center">
                <div class="row">
                    <div class="col">
                        <button type="button" class="btn btn-outline-dark btn-lg">
                            Limpiar Filtros
                        </button>
                    </div>

                    <div class="col">
                        <nav class="navbar">
                            <div class="container-fluid">
                                <form class="d-flex" role="search">
                                    <input
                                        class="form-control me-2"
                                        type="search"
                                        placeholder="Buscar"
                                        aria-label="Search" />
                                    <button
                                        class="btn btn-outline-black"
                                        type="submit">
                                        Search
                                    </button>
                                </form>
                            </div>
                        </nav>
                    </div>

                    <div class="col">
                        <!--RANGO MIN MAX-->
                        <h6 style="color: black">Rango de stock</h6>
                        <div class="row g-3">
                            <div class="col">
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="min"
                                    aria-label="First name" />
                            </div>
                            <div class="col">
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="max"
                                    aria-label="Last name" />
                            </div>
                        </div>
                    </div>

                    <div class="col">
                        <button type="button" class="btn btn-outline-dark btn-lg">
                            Solicitar Nuevo Pedido
                        </button>
                    </div>
                </div>
            </div>

            <!--TABLA DE BODEGAS-->
            <div class="container" style="background-color: white">
                <table class="table table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col">Código del Producto</th>
                            <th scope="col">Descripcion del Producto</th>
                            <th scope="col">Stock</th>
                            <th scope="col">Costo</th>
                            <th scope="col">P.Venta</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>GST00236</th>
                            <td>Calentador Nike</td>
                            <td>10</td>
                            <td>$35.06</td>
                            <td>$37.06</td>
                        </tr>
                        <tr>
                            <th>GST00236</th>
                            <td>Calentador Nike</td>
                            <td>10</td>
                            <td>$35.06</td>
                            <td>$37.06</td>
                        </tr>
                        <tr>
                            <th>GST00236</th>
                            <td>Calentador Nike</td>
                            <td>10</td>
                            <td>$35.06</td>
                            <td>$37.06</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>
