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
                                    Nombre de usuario:
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
                                    Tipo de usuario:
                                </h6>
                                <select
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option selected>Administrador</option>
                                    <option value="1">Gerente</option>
                                    <option value="2">Two</option>
                                    <option value="3">Three</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!--BOTONES-->
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
                                    Enviar a:
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
                                    Estado de cuenta:
                                </h6>
                                <select
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option selected>Activada</option>
                                    <option value="1">Desactivada</option>
                                    <option value="2">Two</option>
                                    <option value="3">Three</option>
                                </select>
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
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Apellidos:
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
                                    Contraseña:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="Last name" />
                            </div>

                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        class="bi bi-trash"
                                        viewBox="0 0 16 16">
                                        <path
                                            d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                                        <path
                                            fill-rule="evenodd"
                                            d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
                                    </svg>
                                    Borrar Usuario
                                </button>
                            </div>

                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        class="bi bi-person"
                                        viewBox="0 0 16 16">
                                        <path
                                            d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z" />
                                    </svg>
                                    Modificar Usuario
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

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
                                    Detalles del Producto:
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
                                    Cantidad del Producto:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="Last name" />
                            </div>

                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        class="bi bi-device-ssd"
                                        viewBox="0 0 16 16">
                                        <path
                                            d="M4.75 4a.75.75 0 0 0-.75.75v3.5c0 .414.336.75.75.75h6.5a.75.75 0 0 0 .75-.75v-3.5a.75.75 0 0 0-.75-.75h-6.5ZM5 8V5h6v3H5Zm0-5.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0Zm7 0a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0ZM4.5 11a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1Zm7 0a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1Z" />
                                        <path
                                            d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2Zm11 12V2a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1v-2a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2a1 1 0 0 0 1-1Zm-7.25 1v-2H5v2h.75Zm1.75 0v-2h-.75v2h.75Zm1.75 0v-2H8.5v2h.75ZM11 13h-.75v2H11v-2Z" />
                                    </svg>
                                    Guardar Usuario
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!--TABLA DE BODEGAS-->
            <div class="container" style="background-color: white">
                <table class="table table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col">Tipo de permiso</th>
                            <th scope="col">Tipo</th>
                            <th scope="col">Activada</th>
                            <th scope="col">Desactivada</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>Administrador de bodega</th>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <th>Administrador de bodega</th>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <th>Administrador de bodega</th>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
                            </td>
                            <td>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault" />
                                </div>
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
