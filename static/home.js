"use strict";

$(document).ready(() => {
    const cupcakeApp = new CupcakeApp();
    cupcakeApp.getCupcakes();
});

class CupcakeApp {
    static IMAGE_WIDTH = 200;

    constructor() {
        $("#form-cupcake").submit(this.createCupcake.bind(this));
        $("#form-search").submit(this.searchCupcakes.bind(this));
    }

    /**
     * Gets a list of cupcakes and displays them on the webpage.
     *
     * @param {String} flavor The cupcake flavor.
     */
    async getCupcakes(flavor) {
        $("#cupcake-list").empty();

        let response;

        try {
            response = await axios.get("/api/cupcakes", { params: { flavor: flavor } });
        } catch (error) {
            displayAPIError(error);
            return;
        }

        for (const cupcake of response.data.cupcakes) {
            $("#cupcake-list").append(this.generateCupcakeHtml(cupcake));
        }
    }

    /**
     * Creates a cupcake and adds it to the database and webpage.
     *
     * @param {Event} e The form submission event for creating a cupcake.
     */
    async createCupcake(e) {
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

        $("#cupcake-list").append(this.generateCupcakeHtml(response.data.cupcake));
    }

    /**
     * Searches for a specified cupcake flavor.
     *
     * @param {Event} e The form submission event for searching a cupcake.
     */
    searchCupcakes(e) {
        e.preventDefault();
        const flavor = $("#form-search__input-flavor").val();
        this.getCupcakes(flavor);
    }

    /**
     * Helper method to create the list item HTML for a cupcake.
     *
     * @param {Object} cupcake The cupcake object containg keys flavor, size, rating, and image.
     * @returns HTML string for the li element, representing a cupcake.
     */
    generateCupcakeHtml(cupcake) {
        return `
        <li>
            <img src="${cupcake.image}" alt="${cupcake.flavor} cupcake image" width="${CupcakeApp.IMAGE_WIDTH}" />
            <p>Flavor: ${cupcake.flavor}</p>
            <p>Size: ${cupcake.size}</p>
            <p>Rating: ${cupcake.rating}</p>
        </li>
        `;
    }
}
