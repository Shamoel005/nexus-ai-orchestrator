import matplotlib.pyplot as plt
import matplotlib.animation as animation
import redis
import json
from collections import Counter
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_stats():
    """Redis se saare results lo"""
    all_results = r.hgetall("results")
    categories = []
    statuses = []
    
    for filename, data in all_results.items():
        parsed = json.loads(data)
        categories.append(parsed.get("category", "unknown"))
        statuses.append(parsed.get("status", "unknown"))
    
    return categories, statuses

def show_dashboard():
    """Live dashboard dikhao"""
    
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Nexus — Document Processing Dashboard', 
                 fontsize=16, color='white', fontweight='bold')
    
    def update(frame):
        categories, statuses = get_stats()
        
        # Saare plots clear karo
        for ax in axes.flat:
            ax.clear()
        
        if not categories:
            for ax in axes.flat:
                ax.text(0.5, 0.5, 'Koi documents nahi abhi...\nPehle koi file upload karo!',
                       ha='center', va='center', color='white', fontsize=12)
            return
        
        category_counts = Counter(categories)
        
        # Plot 1 — Category pie chart
        axes[0, 0].pie(
            category_counts.values(),
            labels=category_counts.keys(),
            autopct='%1.1f%%',
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
        axes[0, 0].set_title('Document Categories', color='white')
        
        # Plot 2 — Bar chart
        axes[0, 1].bar(
            category_counts.keys(),
            category_counts.values(),
            color='#4ECDC4',
            edgecolor='white'
        )
        axes[0, 1].set_title('Category Count', color='white')
        axes[0, 1].tick_params(colors='white')
        axes[0, 1].set_xlabel('Category', color='white')
        axes[0, 1].set_ylabel('Count', color='white')
        
        # Plot 3 — Total processed
        total = len(categories)
        axes[1, 0].text(0.5, 0.6, str(total),
                       ha='center', va='center',
                       fontsize=60, color='#4ECDC4', fontweight='bold')
        axes[1, 0].text(0.5, 0.3, 'Total Documents Processed',
                       ha='center', va='center',
                       fontsize=12, color='white')
        axes[1, 0].set_xlim(0, 1)
        axes[1, 0].set_ylim(0, 1)
        axes[1, 0].axis('off')
        axes[1, 0].set_title('Total Processed', color='white')
        
        # Plot 4 — Queue status
        queue_length = r.llen("task_queue")
        axes[1, 1].text(0.5, 0.6, str(queue_length),
                       ha='center', va='center',
                       fontsize=60, color='#FF6B6B', fontweight='bold')
        axes[1, 1].text(0.5, 0.3, 'Documents in Queue',
                       ha='center', va='center',
                       fontsize=12, color='white')
        axes[1, 1].set_xlim(0, 1)
        axes[1, 1].set_ylim(0, 1)
        axes[1, 1].axis('off')
        axes[1, 1].set_title('Queue Status', color='white')
        
        plt.tight_layout()
    
    # Har 3 second mein update
    ani = animation.FuncAnimation(fig, update, interval=3000)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Dashboard khul raha hai...")
    show_dashboard()