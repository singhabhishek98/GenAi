/**
 * JavaScript for LinkedIn Post Generator
 */

// Load tags when document is ready
$(document).ready(function() {
    loadTags();
    
    // Handle generate button click
    $('#generate').click(function() {
        generatePost();
    });
});

// Function to load tags from API
function loadTags() {
    console.log('Loading tags...');
    
    $.ajax({
        url: '/api/tags',
        method: 'GET',
        timeout: 10000, // 10 second timeout
        success: function(response) {
            console.log('Tags response:', response);
            if (response.success && response.tags && response.tags.length > 0) {
                populateTagsDropdown(response.tags);
            } else {
                console.error('Failed to load tags or no tags found:', response);
                // Add some default tags for testing
                populateTagsDropdown(['Career', 'Technology', 'Business', 'Motivation', 'Leadership']);
                showError('Using default topics. Original data may be loading...');
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', {
                status: status,
                error: error,
                responseText: xhr.responseText,
                xhr: xhr
            });
            // Add default topics as fallback
            populateTagsDropdown(['Career', 'Technology', 'Business', 'Motivation', 'Leadership']);
            showError('Connection error. Using default topics.');
        }
    });
}

// Function to populate tags dropdown
function populateTagsDropdown(tags) {
    const tagSelect = $('#tag');
    
    // Only clear and populate if we have valid tags from API
    if (tags && tags.length > 0) {
        tagSelect.empty(); // Clear existing options
        tagSelect.append('<option value="">Select a topic...</option>');
        
        tags.forEach(function(tag) {
            tagSelect.append(`<option value="${tag}">${tag}</option>`);
        });
        
        console.log('Tags populated from API:', tags.length);
    } else {
        console.log('Using hardcoded topics from HTML');
    }
}

// Function to generate post
function generatePost() {
    const selectedTag = $('#tag').val();
    const selectedLength = $('#length').val();
    const selectedLanguage = $('#language').val();
    const includeEmojis = $('#emojis').is(':checked');
    
    // Validation
    if (!selectedTag) {
        showError('Please select a topic first.');
        return;
    }
    
    // Show loading
    showLoading();
    
    console.log('Generating post with:', {
        tag: selectedTag,
        length: selectedLength,
        language: selectedLanguage,
        include_emojis: includeEmojis
    });
    
    $.ajax({
        url: '/api/generate',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            tag: selectedTag,
            length: selectedLength,
            language: selectedLanguage,
            include_emojis: includeEmojis
        }),
        success: function(response) {
            console.log('Generate response:', response);
            if (response.success) {
                showPost(response.post);
            } else {
                showError('Error: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error generating post:', error);
            showError('An unexpected error occurred while generating the post.');
        }
    });
}

// Function to show loading state
function showLoading() {
    $('#output').html(`
        <div class="alert alert-info">
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            Generating your LinkedIn post... Please wait.
        </div>
    `);
}

// Function to show generated post
function showPost(post) {
    const formattedPost = post.replace(/\n/g, '<br>');
    $('#output').html(`
        <div class="alert alert-success">
            <h5>Generated LinkedIn Post:</h5>
            <hr>
            <p>${formattedPost}</p>
            <hr>
            <button class="btn btn-sm btn-outline-primary" onclick="copyToClipboard()">Copy to Clipboard</button>
        </div>
    `);
}

// Function to show error
function showError(message) {
    $('#output').html(`<div class="alert alert-danger">${message}</div>`);
}

// Function to copy post to clipboard
function copyToClipboard() {
    const postText = $('#output .alert-success p').text();
    navigator.clipboard.writeText(postText).then(function() {
        // Show success message
        const button = $('#output button');
        const originalText = button.text();
        button.text('Copied!').addClass('btn-success').removeClass('btn-outline-primary');
        
        setTimeout(function() {
            button.text(originalText).removeClass('btn-success').addClass('btn-outline-primary');
        }, 2000);
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        alert('Could not copy to clipboard. Please copy manually.');
    });
}
