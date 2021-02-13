<template>
    <b-container>
        <br>
        <h3>Detalles del evento</h3>
        <b-list-group v-if="!editMode">
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Nombre:</b></b-col>
                        <b-col>{{event.name}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Creado el:</b></b-col>
                        <b-col>{{event.created_at}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Lugar:</b></b-col>
                        <b-col>{{event.location}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Dirección:</b></b-col>
                        <b-col>{{event.address}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Fecha de inicio:</b></b-col>
                        <b-col>{{event.start_date}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Fecha de finalización:</b></b-col>
                        <b-col>{{event.end_date}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Tipo:</b></b-col>
                        <b-col>{{eventType}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Modalidad:</b></b-col>
                        <b-col>{{eventModality}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
        </b-list-group>

        <b-list-group v-if="editMode">
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Nombre:</b></b-col>
                        <b-col><b-form-input v-model="editedEvent.name" type="text" :state="nameOK"></b-form-input></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Creado el:</b></b-col>
                        <b-col>{{event.created_at}}</b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Lugar:</b></b-col>
                        <b-col><b-form-input v-model="editedEvent.location" type="text" :state="locationOK"></b-form-input></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Dirección:</b></b-col>
                        <b-col><b-form-input v-model="editedEvent.address" type="text" :state="addressOK"></b-form-input></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Fecha de inicio:</b></b-col>
                        <b-col><b-form-input v-model="editedEvent.start_date" type="date"></b-form-input></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Fecha de finalización:</b></b-col>
                        <b-col><b-form-input v-model="editedEvent.end_date" type="date"></b-form-input></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Tipo:</b></b-col>
                        <b-col><b-form-select v-model="editedEvent.category_id" :options="category_options"></b-form-select></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
            <b-list-group-item>
                <b-container>
                    <b-row>
                        <b-col cols=3><b>Modalidad:</b></b-col>
                        <b-col><b-form-select v-model="editedEvent.online" :options="online_options"></b-form-select></b-col>
                    </b-row>
                </b-container>
            </b-list-group-item>
        </b-list-group>

        <br>
        <b-button variant="primary" v-if="!editMode" @click="toggleEditMode">Editar</b-button>
        <b-button class="btn" variant="success" v-if="editMode" @click="onSubmit">Confirmar cambios</b-button>
        <b-button class="btn" variant="danger" v-if="editMode" @click="toggleEditMode">Cancelar</b-button>
        <br><br>
        <router-link to="/">Volver a lista de eventos</router-link>

        <b-modal ok-only no-close-on-esc no-close-on-backdrop hide-header-close id="ev-edit" title="Editar evento">
        <p class="my-4">{{alert_msg}}</p>
        </b-modal>
    </b-container>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
    data() {
        return {
            event: {},
            editedEvent: {},
            editMode: false,
            category_options: [
                { value: 1, text: 'Conferencia' },
                { value: 2, text: 'Seminario' },
                { value: 3, text: 'Congreso' },
                { value: 4, text: 'Curso' }
            ],
            online_options: [
                { value: false, text: 'Presencial'},
                { value: true,  text: 'Virtual'}
            ],
            alert_msg: ''
        }
    },
    created() {
        this.fetchEventDetails();
    },
    computed: {
        nameOK() {
            return this.editedEvent.name.length > 0 ? true : false
        },
        locationOK() {
            return this.editedEvent.location.length > 0 ? true : false
        },
        addressOK() {
            return this.editedEvent.address.length > 0 ? true : false
        },
        ...mapState([
            'loggedUser'
        ]),
        eventType() {
            if (this.event.category_id == 1) {
                return 'Conferencia';
            }
            if (this.event.category_id == 2) {
                return 'Seminario';
            }
            if (this.event.category_id == 3) {
                return 'Congreso';
            }
            return 'Curso'  
        },
        eventModality() {
            return this.event.online ? 'Virtual' : 'Presencial'
        }
    },
    methods: {
        toggleEditMode() {
            this.editMode = !this.editMode;
            this.editedEvent = JSON.parse(JSON.stringify(this.event))
        },
        fetchEventDetails() {
            var url = 'http://172.24.98.165/event/' + this.$route.params.event_id;
            axios.get(url, {headers: {'Authorization': 'Bearer ' + this.loggedUser.token}}).then(res => {
                this.event = res.data;
                this.event.start_date = this.event.start_date.substring(0, 10);
                this.event.end_date = this.event.end_date.substring(0, 10);
            }).catch(err => {
                console.log(err);
            });
        },
        onSubmit() {
            if (!this.nameOK || !this.locationOK || !this.addressOK) {
                this.alert_msg = 'Favor llenar todos los campos.';
                this.$bvModal.show("ev-edit");
            }
            else {
                var url = 'http://172.24.98.165/event/' + this.event.id;
                axios.put(url, this.editedEvent, {headers: {'Authorization': 'Bearer ' + this.loggedUser.token}}).then(res => {
                    this.alert_msg = 'Se ha editado el evento exitosamente!';
                    this.$bvModal.show("ev-edit");
                    this.event = res.data;
                    this.event.start_date = this.event.start_date.substring(0, 10);
                    this.event.end_date = this.event.end_date.substring(0, 10);
                    this.editMode = !this.editMode;
                }).catch(err => {
                    this.alert_msg = 'Error: no se pudo editar el evento. Favor intentar de nuevo.'
                    this.$bvModal.show("ev-edit");
                })
            }
        }
    }
}
</script>

<style scoped>
.btn {
  margin: 0 5px;
}
</style>