require "rubygems"
require 'rake'
require 'yaml'
require 'time'
require "rake/clean"
require "stringex"

SOURCE = "."
CONFIG = {
  'layouts' => File.join(SOURCE, "_layouts"),
  'posts' => File.join(SOURCE, "_posts"),
  'post_ext' => "md"
}

desc 'List available rake tasks'
task :default do
  puts 'Try one of these specific tasks:'
  sh 'rake --tasks --silent'
end

# Usage: rake page name="about.md"
# You can also specify a sub-directory path.
# If you don't specify a file extention we create an index.html at the path specified
desc "Create a new page."
task :page do
  name = ENV["name"] || "new-page.md"
  filename = File.join(SOURCE, "#{name}")
  filename = File.join(filename, "index.html") if File.extname(filename) == ""
  title = File.basename(filename, File.extname(filename)).gsub(/[\W\_]/, " ").gsub(/\b\w/){$&.upcase}
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end

  mkdir_p File.dirname(filename)
  puts "Creating new page: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: page"
    post.puts "group: "
    post.puts "title: \"#{title}\""
    post.puts "permalink: "
    post.puts 'description: ""'
    post.puts "---"
  end
end # task :page

desc "Write a new post"
task :write do |t|

  title    = get_stdin("What is the title of your post? ")
  filename = "_posts/#{Time.now.strftime('%Y-%m-%d')}-#{title.to_url}.markdown"

  puts "Creating new draft: #{filename}"
  open(filename, "w") do |post|
    post.puts "---"
    post.puts "layout: page"
    post.puts "title: \"#{title.gsub(/&/,'&amp;')}\""
    post.puts "date: #{Time.now.strftime('%Y-%m-%d %H:%M')}"
    post.puts "categories: news"
    post.puts "---"
  end
end

desc "Create a new event"
task :event do |t|

  title    = get_stdin("What is the title of your event? ")
  dateTime = get_stdin("What is the date of your event (YYYY-MM-DD)? ")
  filename = "_posts/#{dateTime}-event-#{title.to_url}.markdown"

  puts "Creating a new event: #{filename}"
  open(filename, "w") do |post|
    post.puts "---"
    post.puts "layout: page"
    post.puts "title: \"#{title.gsub(/&/,'&amp;')}\""
    post.puts "date: #{dateTime} #{Time.now.strftime('%H:%M')}"
    post.puts "categories: event"
    post.puts "---"
  end
end

desc "Run the development server."
task :preview do
  sh "jekyll server --watch"
end

desc "Nuke and rebuild."
task :nuke do
    sh 'rm -rf _site'
    system "jekyll build"
end

def get_stdin(message)
  print message
  STDIN.gets.chomp
end
