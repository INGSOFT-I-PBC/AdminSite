<template>
    <main>
        <ECard> </ECard>

        <div
            class="container"
            style="
                background-color: white;
                border-radius: 5px;
            ">
            <!--BOTONES Usuario-->
            <div
                class="container text-center"
                style="padding: 10px">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <h6
                                style="
                                    font-weight: bold;
                                    font-size: 15px;
                                    text-align: left;
                                    color: black;
                                ">
                                Informacion
                                General
                            </h6>
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Razon social:
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
                                    Tipo de
                                    identificacion:
                                </h6>
                                <select
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option
                                        selected>
                                        Todos
                                    </option>
                                    <option
                                        value="1">
                                        Gerente
                                    </option>
                                    <option
                                        value="2">
                                        Two
                                    </option>
                                    <option
                                        value="3">
                                        Three
                                    </option>
                                </select>
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Numero de
                                    identificacion:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
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
                        </div>
                    </div>
                </div>
            </div>

            <!--BOTONES Usuario-->
            <div
                class="container text-center"
                style="padding: 10px">
                <div class="row">
                    <div class="col">
                        <div class="row g-3">
                            <h6
                                style="
                                    font-weight: bold;
                                    font-size: 15px;
                                    text-align: left;
                                    color: black;
                                ">
                                Ubicacion
                            </h6>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Pais:
                                </h6>
                                <select
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option
                                        selected>
                                        Ecuador
                                    </option>
                                    <option
                                        value="1">
                                        Gerente
                                    </option>
                                    <option
                                        value="2">
                                        Two
                                    </option>
                                    <option
                                        value="3">
                                        Three
                                    </option>
                                </select>
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Direccion
                                    Fisica:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name" />
                            </div>
                        </div>

                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Ciudad:
                                </h6>
                                <select
                                    class="form-select"
                                    aria-label="Default select example">
                                    <option
                                        selected>
                                        Guayaquil
                                    </option>
                                    <option
                                        value="1">
                                        Gerente
                                    </option>
                                    <option
                                        value="2">
                                        Two
                                    </option>
                                    <option
                                        value="3">
                                        Three
                                    </option>
                                </select>
                            </div>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Direccion
                                    Envio:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name" />
                            </div>
                        </div>

                        <!--Espacio demas-->
                        <div
                            class="container text-center"
                            style="
                                padding: 10px;
                            "></div>

                        <div class="row g-3">
                            <h6
                                style="
                                    font-weight: bold;
                                    font-size: 15px;
                                    text-align: left;
                                    color: black;
                                ">
                                Contacto
                            </h6>

                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Nombre
                                    contacto
                                    principal:
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
                                    Sitio Web:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name" />
                            </div>
                        </div>

                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Telefono:
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
                                    Correo
                                    Electronico:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name" />
                            </div>
                        </div>

                        <div class="row g-3">
                            <div class="col">
                                <h6
                                    style="
                                        font-size: 15px;
                                        color: black;
                                        text-align: left;
                                    ">
                                    Fax:
                                </h6>
                                <input
                                    type="text"
                                    class="form-control"
                                    placeholder=""
                                    aria-label="First name" />
                            </div>
                        </div>

                        <div
                            class="row g-3"
                            style="padding: 10px">
                            <div class="col">
                                <button
                                    type="button"
                                    class="btn btn-outline-dark">
                                    Guardar
                                    Informacion
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!--Espacio demas-->
            <div
                class="container text-center"
                style="padding: 10px"></div>
        </div>
    </main>
</template>
