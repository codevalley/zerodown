"""
Main builder module for the Zerodown static site generator.
"""

import os
import sys
import datetime
import time
from pathlib import Path

from zerodown.utils import clean_output_dir, copy_static_assets, copy_styles
from zerodown.templates import setup_jinja_env, process_includes
from zerodown.content import process_section, build_homepage, process_top_level_pages
from zerodown.markdown import copy_content_assets
from zerodown.console import zconsole


def build_site(config):
    """
    Main function to build the entire static site.
    
    Args:
        config: Configuration module with site settings
        
    Returns:
        bool: True if build was successful
    """
    start_time = datetime.datetime.now()
    
    # Display site info
    site_name = getattr(config, 'SITE_NAME', 'Zerodown Site')
    zconsole.header(f"Building {site_name}")
    
    # Start progress tracking
    main_task = zconsole.start_progress("Building site")
    
    try:
        # 1. Setup
        setup_task = zconsole.add_subtask("Setting up environment")
        zconsole.update_progress(setup_task, status="Cleaning output directory")
        clean_output_dir(config)  # Exits on error
        
        zconsole.update_progress(setup_task, status="Copying static assets", advance=25)
        copy_static_assets(config)  # Continues on error
        
        zconsole.update_progress(setup_task, status="Applying theme", advance=25)
        copy_styles(config)  # Continues on error
        
        zconsole.update_progress(setup_task, status="Setting up templates", advance=25)
        jinja_env = setup_jinja_env(config)  # Exits on error
        
        zconsole.update_progress(setup_task, status="Complete", advance=25)
        
        # 2. Process includes for global template context
        includes_task = zconsole.add_subtask("Processing includes")
        process_includes(config, jinja_env)
        zconsole.update_progress(includes_task, status="Complete", advance=100)
        
        # 3. Copy assets from content directory
        assets_task = zconsole.add_subtask("Copying content assets")
        copy_content_assets(config)
        zconsole.update_progress(assets_task, status="Complete", advance=100)
    
        # 4. Process all sections
        all_items = []  # To collect items from all sections for homepage
        
        if not hasattr(config, 'SECTIONS') or not isinstance(config.SECTIONS, dict):
            zconsole.error("'SECTIONS' dictionary not found or invalid in config")
            sys.exit(1)
    
        section_count = len(config.SECTIONS)
        for i, (section_key, section_config) in enumerate(config.SECTIONS.items()):
            section_title = section_config.get('title', section_key.capitalize())
            section_task = zconsole.add_subtask(f"Processing section: {section_title}")
            
            # Process the section
            section_items = process_section(config, jinja_env, section_key, section_config, all_items)
            
            # Update progress
            progress_percent = 100
            zconsole.update_progress(section_task, 
                                    status=f"Built {len(section_items)} items", 
                                    advance=progress_percent)
            
            # Update main progress based on section completion
            main_progress = (i + 1) / (section_count + 2) * 100  # +2 for homepage and top-level pages
            zconsole.update_progress(main_task, status=f"Processing sections ({i+1}/{section_count})", advance=main_progress)
    
        # 5. Build top-level pages
        pages_task = zconsole.add_subtask("Building top-level pages")
        
        zconsole.update_progress(pages_task, status="Building homepage", advance=50)
        build_homepage(config, jinja_env, all_items)
        
        zconsole.update_progress(pages_task, status="Building other pages", advance=50)
        process_top_level_pages(config, jinja_env)
        
        # Update main progress
        zconsole.update_progress(main_task, status="Finalizing")
    
        # 6. Finish and report
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        # Stop progress display
        zconsole.stop_progress()
        
        # Show build summary
        stats = {
            "Build Duration": f"{duration.total_seconds():.2f} seconds",
            "Total Pages": len(all_items) + 2,  # +2 for homepage and about page (estimate)
            "Sections": len(config.SECTIONS),
            "Output Directory": config.OUTPUT_DIR
        }
        
        zconsole.success(f"Site build complete!")
        zconsole.display_summary(stats)
        
        # Show output files tree if not too many files
        output_path = Path(config.OUTPUT_DIR)
        if output_path.exists():
            files = [str(f.relative_to(output_path)) for f in output_path.glob('**/*') if f.is_file()]
            if len(files) <= 20:  # Only show tree if not too many files
                zconsole.display_file_tree("Generated Files", config.OUTPUT_DIR, files)
        
        return True
        
    except Exception as e:
        zconsole.stop_progress()
        zconsole.error(f"Build failed: {str(e)}")
        import traceback
        zconsole.error(traceback.format_exc())
        return False
