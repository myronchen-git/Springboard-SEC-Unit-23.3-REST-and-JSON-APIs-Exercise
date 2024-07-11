"use strict";

$(document).ready(() => {
    new CupcakeApp();
    CupcakeApp.getCupcakes();
});

class CupcakeApp {
    static IMAGE_WIDTH = 200;

    constructor() {
        $("#form-cupcake").submit(CupcakeApp.createCupcake.bind(this));
        $("#form-search").submit(this.searchCupcakes.bind(this));
        $("#cupcake-list").on("click", "button.delete-cupcake", this.deleteCupcake);
        $("#cupcake-list").on("click", "button.edit-cupcake", this.showEditForm);
        $("#cupcake-list").on("click", "button.form-edit-cupcake__submit", this.updateCupcake);
    }

    /**
     * Gets a list of cupcakes and displays them on the webpage.
     *
     * @param {String} flavor The cupcake flavor.
     */
    static async getCupcakes(flavor) {
        $("#cupcake-list").empty();

        let response;
        try {
            response = await axios.get("/api/cupcakes", { params: { flavor: flavor } });
        } catch (error) {
            displayAPIError(error);
            return;
        }

        for (const cupcake of response.data.cupcakes) {
            $("#cupcake-list").append(CupcakeApp.generateCupcakeHtml(cupcake));
        }
    }

    /**
     * Creates a cupcake and adds it to the database and webpage.
     *
     * @param {Event} e The form submission event for creating a cupcake.
     */
    static async createCupcake(e) {
        e.preventDefault();

        const flavor = $("#form-cupcake__input-flavor").val();
        const size = $("#form-cupcake__input-size").val();
        const rating = $("#form-cupcake__input-rating").val();
        const image = $("#form-cupcake__input-image").val() || null;

        let response;
        try {
            response = await axios.post("/api/cupcakes", {
                flavor: flavor,
                size: size,
                rating: rating,
                image: image,
            });
            console.log("Successfully submitted cupcake.");
        } catch (error) {
            displayAPIError(error);
            return;
        }

        $("#form-cupcake").get(0).reset();

        $("#cupcake-list").append(CupcakeApp.generateCupcakeHtml(response.data.cupcake));
    }

    /**
     * Searches for a specified cupcake flavor.
     *
     * @param {Event} e The form submission event for searching a cupcake.
     */
    searchCupcakes(e) {
        e.preventDefault();
        const flavor = $("#form-search__input-flavor").val();
        CupcakeApp.getCupcakes(flavor);
    }

    // can be refactored
    /**
     * Displays the form to edit a cupcake's info.
     */
    showEditForm() {
        const $cupcakeListItem = $(this.closest("li[data-cupcake-id]"));
        const cupcakeId = $cupcakeListItem.data("cupcake-id");

        $cupcakeListItem.children(":not(:first-child)").remove();
        $cupcakeListItem.append(`
            <form id="form-edit-cupcake-${cupcakeId}">
                <div>
                    <label for="form-edit-cupcake-${cupcakeId}__input-flavor">Flavor:</label>
                    <input id="form-edit-cupcake-${cupcakeId}__input-flavor" type="text" name="flavor" required />
                </div>
                <div>
                    <label for="form-edit-cupcake-${cupcakeId}__input-size">Size:</label>
                    <input id="form-edit-cupcake-${cupcakeId}__input-size" type="text" name="size" required />
                </div>
                <div>
                    <label for="form-edit-cupcake-${cupcakeId}__input-rating">Rating:</label>
                    <input id="form-edit-cupcake-${cupcakeId}__input-rating" type="number" name="rating" required />
                </div>
                <div>
                    <label for="form-edit-cupcake-${cupcakeId}__input-image">Image:</label>
                    <input id="form-edit-cupcake-${cupcakeId}__input-image" type="url" name="image" />
                </div>
                <button class="form-edit-cupcake__submit" type="submit">Submit</button>
            </form>
            `);
    }

    /**
     *
     * @param {Event} e The form submission event for updating a cupcake.
     * @returns
     */
    async updateCupcake(e) {
        const $cupcakeListItem = $(this.closest("li[data-cupcake-id]"));
        const cupcakeId = $cupcakeListItem.data("cupcake-id");

        const validity = $(this.closest("form"))[0].reportValidity();
        if (validity) {
            e.preventDefault();

            const flavor = $(`#form-edit-cupcake-${cupcakeId}__input-flavor`).val();
            const size = $(`#form-edit-cupcake-${cupcakeId}__input-size`).val();
            const rating = $(`#form-edit-cupcake-${cupcakeId}__input-rating`).val();
            const image = $(`#form-edit-cupcake-${cupcakeId}__input-image`).val();

            const data = {};

            for (const [field, value] of Object.entries({ flavor, size, rating, image })) {
                if (value) {
                    data[field] = value;
                }
            }

            let response;
            try {
                response = await axios.patch(`/api/cupcakes/${cupcakeId}`, data);
                console.log("Successfully updated cupcake.");
            } catch (error) {
                displayAPIError(error);
                return;
            }

            $cupcakeListItem.replaceWith(CupcakeApp.generateCupcakeHtml(response.data.cupcake));
        }
    }

    /**
     * Deletes a cupcake from both the database and webpage.
     */
    async deleteCupcake() {
        const $cupcakeListItem = $(this.closest("li[data-cupcake-id]"));
        const cupcakeId = $cupcakeListItem.data("cupcake-id");

        let response;
        try {
            response = await axios.delete(`/api/cupcakes/${cupcakeId}`);
            console.log(
                `Successfully deleted cupcake.\nResponse message: "${response.data.message}"`
            );
        } catch (error) {
            displayAPIError(error);
            return;
        }

        $cupcakeListItem.remove();
    }

    /**
     * Helper method to create the list item HTML for a cupcake.
     *
     * @param {Object} cupcake The cupcake object containg keys flavor, size, rating, and image.
     * @returns HTML string for the li element, representing a cupcake.
     */
    static generateCupcakeHtml(cupcake) {
        return `
        <li data-cupcake-id="${cupcake.id}">
            <img src="${cupcake.image}" alt="${cupcake.flavor} cupcake image" width="${CupcakeApp.IMAGE_WIDTH}" />
            <p>Flavor: ${cupcake.flavor}</p>
            <p>Size: ${cupcake.size}</p>
            <p>Rating: ${cupcake.rating}</p>
            <div>
                <button class="edit-cupcake" type="button">Edit</button>
                <button class="delete-cupcake" type="button">X</button>
            </div>
        </li>
        `;
    }
}
