<template>
    <main>
        <ECard> </ECard>

        <div
            class="container"
            style="
                background-color: white;
                border-radius: 5px;
            ">
            <div
                class="container"
                style="
                    background-color: white;
                    padding: 10px;
                ">
                <h6
                    style="
                        font-size: 15px;
                        color: black;
                    ">
                    Enviar a:
                </h6>

                <select
                    class="form-select"
                    aria-label="Default select example">
                    <option selected>
                        Seleccione sucursal o
                        bodega
                    </option>
                    <option value="1">One</option>
                    <option value="2">Two</option>
                    <option value="3">
                        Three
                    </option>
                </select>
            </div>

            <div
                class="btn-group"
                role="group"
                aria-label="Basic radio toggle button group"
                style="padding: 10px">
                <button
                    type="button"
                    class="btn btn-outline-dark btn-lg">
                    Seleccionar Producto
                </button>
            </div>

            <!--DIV DE BOTONES Y NAV-->
            <div class="container text-center">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <div class="col">
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="Nombre Producto"
                                    aria-label="First name" />
                            </div>

                            <div class="col">
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="Codigo Producto"
                                    aria-label="Last name" />
                            </div>

                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark">
                                    Añadir
                                    Producto
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div
                class="container text-center"
                style="padding: 10px">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <div class="col">
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="Detalles del Producto"
                                    aria-label="First name" />
                            </div>

                            <div class="col">
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="Cantidad del Producto"
                                    aria-label="Last name" />
                            </div>

                            <div
                                class="col"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!--TABLA DE BODEGAS-->
            <div
                class="container"
                style="background-color: white">
                <table
                    class="table table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col">
                                Nombre del
                                Producto
                            </th>
                            <th scope="col">
                                Codigo
                            </th>
                            <th scope="col">
                                Cantidad
                            </th>
                            <th scope="col">
                                Detalles
                            </th>
                            <th scope="col">
                                Eliminacion
                            </th>
                            <th scope="col">
                                Detalles
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>
                                Zapatos marca x
                            </th>
                            <td>102 WFP WNGE</td>
                            <td>100</td>
                            <td>N/A</td>
                            <td>--</td>
                            <td>--</td>
                        </tr>
                        <tr>
                            <th>
                                Zapatos marca x
                            </th>
                            <td>102 WFP WNGE</td>
                            <td>100</td>
                            <td>N/A</td>
                            <td>--</td>
                            <td>--</td>
                        </tr>
                        <tr>
                            <th>
                                Zapatos marca x
                            </th>
                            <td>102 WFP WNGE</td>
                            <td>100</td>
                            <td>N/A</td>
                            <td>--</td>
                            <td>--</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!--Enviar Solicitud-->
            <div
                class="container text-center"
                style="padding: 10px">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark btn-lg">
                                    Enviar
                                    Solicitud
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
