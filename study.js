$(document).ready(function () {
    // Apply search prevention to the search form on all pages
    preventWhitespaceSearch('#searchForm');

    // Check if we're on the search results page
    if ($("#search-results").length > 0) {
        // Get query from the page
        let query = $("#result-count").text().match(/"([^"]+)"/);

        if (query && query[1]) {
            query = query[1].trim();

            $("#search-results li a").each(function () {
                let originalText = $(this).text();
                let highlightedText = highlightMatch(originalText, query);
                $(this).html(highlightedText);
            });

            // Add visual grouping for results with matches
            $("#search-results li").each(function () {
                if ($(this).find("mark").length > 0) {
                    $(this).addClass("strong-match");
                }
            });
        }
    }

    // Check if we're on the view page and if there's a search query in URL
    if ($(".container h2").length > 0 && window.location.search.includes('q=')) {
        // Extract query from URL
        let urlParams = new URLSearchParams(window.location.search);
        let query = urlParams.get('q');

        if (query) {
            // Apply highlighting to appropriate content in view.html
            $(".col-md-6 p").each(function () {
                let $strong = $(this).find("strong");

                if ($strong.length > 0) {
                    let textContent = $(this).contents().filter(function() {
                        return this.nodeType === 3; // Text nodes only
                    });

                    // Process each text node
                    textContent.each(function() {
                        let text = this.nodeValue;
                        let highlightedText = highlightMatch(text, query);

                        // Replace text node with highlighted content
                        if (text !== highlightedText) {
                            $(this).replaceWith(highlightedText);
                        }
                    });
                } else {
                    // If no strong element, process the entire content
                    let text = $(this).text();
                    let highlightedText = highlightMatch(text, query);
                    $(this).html(highlightedText);
                }
            });

            // Also highlight the title if it matches
            let titleText = $(".container h2").text();
            let highlightedTitle = highlightMatch(titleText, query);
            $(".container h2").html(highlightedTitle);
        }
    }

    // If on home page and spots are defined, display them
    if (typeof spots !== 'undefined') {
        displaySpot(spots);
    }

    // Set focus on the name field when the add page loads
    if ($("#addForm").length) {
        $("#name").focus();
    }

    $("#addForm").submit(function (event) {
        event.preventDefault();

        let formData = {
            name: $("#name").val().trim(),
            location: $("#location").val().trim(),
            description: $("#description").val().trim(),
            capacity: $("#capacity").val().trim(),
            time: $("#time").val().trim(),
            image: $("#image").val().trim(),
            noise_level: $("#noise_level").val().trim(),
            wifi: $("#wifi").val().trim(),
            outlets: $("#outlets").val().trim(),
            related_topics: $("#related_topics").val().trim(),
        };
        // Clear previous error messages
        $(".form-control").removeClass("is-invalid");
        $(".invalid-feedback").text("");

        // Send data using AJAX
        $.ajax({
            type: "POST",
            url: "/submit",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (response) {
                // Show success message
                $("#success-message").removeClass("d-none");
                $("#view-link").attr("href", `/view/${response.id}`);

                // Clear form fields
                $("#addForm")[0].reset();

                // Focus first input field
                $("#name").focus();
            },
            error: function (xhr) {
                let errors = xhr.responseJSON.errors;
                let firstErrorField = null;

                // Define the form fields in proper order to ensure focus goes to the first error
                let fieldOrder = ["name", "location", "description", "capacity", "time", "image",
                                 "noise_level", "wifi", "outlets", "related_topics"];

                // Check fields in order and find the first one with an error
                for (let field of fieldOrder) {
                    if (errors[field]) {
                        let inputField = $("#" + field);
                        inputField.addClass("is-invalid");
                        inputField.next(".invalid-feedback").text(errors[field]);

                        if (!firstErrorField) {
                            firstErrorField = inputField;
                        }
                    }
                }

                // Focus the first field with an error
                if (firstErrorField) {
                    firstErrorField.focus();
                }
            }
        });
    });

   $("#editForm").submit(function (event) {
        event.preventDefault();

        let formData = {
            name: $("#name").val().trim(),
            location: $("#location").val().trim(),
            description: $("#description").val().trim(),
            capacity: $("#capacity").val().trim(),
            time: $("#time").val().trim(),
            image: $("#image").val().trim(),
            noise_level: $("#noise_level").val().trim(),
            wifi: $("#wifi").val().trim(),
            outlets: $("#outlets").val().trim(),
            related_topics: $("#related_topics").val().trim(),
        };

        let itemId = $("#editForm").data("item-id"); // Get ID from HTML

        $.ajax({
            url: "/update/" + itemId,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (response) {
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    alert("Update successful, but no redirect URL provided.");
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
                alert("Failed to update. Please try again.");
            }
        });
    });

    // Fix the double confirmation by using one click handler
    // Only attach the click handler if the discardBtn exists on the page
    if ($("#discardBtn").length) {
        $("#discardBtn").off("click").on("click", function() {
            if (confirm("Are you sure you want to discard changes? Your edits will not be saved.")) {
                let itemId = $(this).data("item-id"); // Get ID from button attribute
                window.location.href = "/view/" + itemId;
            }
        });
    }
});

function highlightMatch(text, query) {
    if (!text || !query) return text;

    let safeQuery = query.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    let regex = new RegExp(`(${safeQuery})`, 'gi');

    return text.replace(regex, '<mark class="highlight-match">$1</mark>');
}

function preventWhitespaceSearch(formSelector) {
    $(formSelector).submit(function (e) {
        let searchInput = $(this).find('#searchInput');
        let query = searchInput.val().trim();

        if (!query) {
            e.preventDefault();
            searchInput.val('');
            searchInput.focus();
            return false;
        }
    });
}

function displaySpot(spots) {
    $("#popular-spots").empty();

    spots.forEach(function (item) {
        let spot = $(
            `<div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100">
                    <div class="p-3">
                        <a href="/view/${item.id}" class="text-decoration-none">
                            <h4>${item.name}</h4>
                        </a>
                        <span>${item.time || ''}</span>
                        <a href="/view/${item.id}">
                            <img src="${item.image}" alt="${item.name}" class="img-fluid rounded">
                        </a>
                        <div class="mt-2">
                            <small class="text-muted">${item.location}</small>
                        </div>
                    </div>
                </div>
            </div>`
        );
        $("#popular-spots").append(spot);
    });
}