<template>
    <main>
        <ECard> </ECard>

        <div
            class="container"
            style="background-color: white; border-radius: 5px">
            <!--BOTONES Usuario-->
            <div class="container text-center" style="padding: 10px">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Tipo de Movimiento:
                                </h6>
                                <select
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option selected>Todos</option>
                                    <option value="1">Gerente</option>
                                    <option value="2">Two</option>
                                    <option value="3">Three</option>
                                </select>
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Descripcion:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name" />
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Cantidad de items:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="min"
                                    aria-label="First name" />
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="max"
                                    aria-label="First name" />
                            </div>

                            <div class="col" style="padding: 5px">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Rango de horas:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="inicio"
                                    aria-label="First name" />
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="fin"
                                    aria-label="First name" />
                            </div>

                            <div class="col" style="padding: 5px">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Rango de fechas:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="inicio"
                                    aria-label="First name" />
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder="fin"
                                    aria-label="First name" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!--DIV DE BOTONES Y NAV-->
            <div class="container text-center">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark">
                                    Limpiar Filtros
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container text-center" style="padding: 10px"></div>

            <!--TABLA DE BODEGAS-->
            <div class="container" style="background-color: white">
                <table class="table table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col">Tipo</th>
                            <th scope="col">Descripcion Movimiento</th>
                            <th scope="col">Nombre Inventario</th>
                            <th scope="col">Inventario Movido</th>
                            <th scope="col">Hora</th>
                            <th scope="col">Fecha</th>
                            <th scope="col">Detalles</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>Salida</th>
                            <td>Movimiento a local</td>
                            <td>Bodega 1</td>
                            <td>100</td>
                            <td>00:30 am</td>
                            <td>12/02/22</td>
                            <td>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    fill="currentColor"
                                    class="bi bi-file-earmark"
                                    viewBox="0 0 16 16">
                                    <path
                                        d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z" />
                                </svg>
                            </td>
                        </tr>
                        <tr>
                            <th>Salida</th>
                            <td>Movimiento a local</td>
                            <td>Bodega 1</td>
                            <td>100</td>
                            <td>00:30 am</td>
                            <td>12/02/22</td>
                            <td>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    fill="currentColor"
                                    class="bi bi-file-earmark"
                                    viewBox="0 0 16 16">
                                    <path
                                        d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z" />
                                </svg>
                            </td>
                        </tr>
                        <tr>
                            <th>Salida</th>
                            <td>Movimiento a local</td>
                            <td>Bodega 1</td>
                            <td>100</td>
                            <td>00:30 am</td>
                            <td>12/02/22</td>
                            <td>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    fill="currentColor"
                                    class="bi bi-file-earmark"
                                    viewBox="0 0 16 16">
                                    <path
                                        d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z" />
                                </svg>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!--Espacio demas-->
            <div class="container text-center" style="padding: 10px"></div>
        </div>
    </main>
</template>
