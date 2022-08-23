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
                <h1
                    style="
                        font-size: 35px;
                        color: black;
                    ">
                    Bodegas
                </h1>

                <nav class="navbar">
                    <div class="container-fluid">
                        <form
                            class="d-flex"
                            role="search">
                            <input
                                class="form-control me-2"
                                type="search"
                                placeholder="Busqueda de Bodega"
                                aria-label="Search" />
                            <button
                                class="btn btn-outline-black"
                                type="submit">
                                Search
                            </button>
                        </form>
                    </div>
                </nav>

                <button
                    type="button"
                    class="btn btn-light d-inline"
                    data-bs-container="body"
                    data-bs-toggle="popover"
                    data-bs-placement="top"
                    data-bs-content="Top popover">
                    Modificar Bodega
                </button>
                <button
                    type="button"
                    class="btn btn-light"
                    data-bs-container="body"
                    data-bs-toggle="popover"
                    data-bs-placement="right"
                    data-bs-content="Right popover">
                    Eliminar Bodega
                </button>
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
                                Código Bodega
                            </th>
                            <th scope="col">
                                Ubicación
                            </th>
                            <th scope="col">
                                Fecha última toma
                                física
                            </th>
                            <th scope="col">
                                Realizada por
                            </th>
                            <th scope="col">
                                Estado
                            </th>
                            <th scope="col">
                                Detalles
                            </th>
                            <th scope="col">
                                Archivos
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>BO-0001</th>
                            <td>centro</td>
                            <td>25-02-22</td>
                            <td>Jose J</td>
                            <td>Draft</td>
                            <td>Icono</td>
                            <td>Icono</td>
                        </tr>
                        <tr>
                            <th>BO-0001</th>
                            <td>centro</td>
                            <td>25-02-22</td>
                            <td>Jose J</td>
                            <td>Draft</td>
                            <td>Icono</td>
                            <td>Icono</td>
                        </tr>
                        <tr>
                            <th>BO-0001</th>
                            <td>centro</td>
                            <td>25-02-22</td>
                            <td>Jose J</td>
                            <td>Draft</td>
                            <td>Icono</td>
                            <td>Icono</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>
