module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            dist: {
                src: ['node_modules/@popperjs/core/dist/umd/popper.min.js', 'node_modules/bootstrap/dist/js/collapse.js', 'src/base.js'],
                dest: 'dist/base.js'
            }
        },
        uglify: {
            options: {
                mangle: true,
                compress: true,
                beautify: false
            },
            dist: {
                files: {
                    '../static/js/base.min.js': ['<%= concat.dist.dest %>'],
                }
            }
        },
        sass: {                              // Task
            dist: {                            // Target
                files: {                         // Dictionary of files
                    'dist/base.css': 'src/base.scss'
                }
            }
        },
        cssmin: {
            target: {
                files: [{
                    expand: true,
                    cwd: 'dist',
                    src: ['*.css', '!*.min.css'],
                    dest: '../static/css',
                    ext: '.min.css'
                }]
            }
        },
        watch: {
            scripts: {
                files: 'src/*.*',
                tasks: ['concat', 'uglify', 'sass', 'cssmin'],
                options: {
                    livereload: true
                },
            },
        }
    });

    // Load the plugins
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Default task(s).

    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin', 'watch']);
    // grunt.registerTask('default', ['sass', 'watch']);

};