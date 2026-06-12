import type { Author, Project} from '@/types'


export const author: Author = {
    name: 'AdoruKw',
    avatar: 'https://picsum.photos/seed/avatar/200/200',
    bio: '一个热爱编程和游戏的开发者，正在探索像素艺术与Web开发的结合。',
    location: '中国',
    social: {
        github: 'https://github.com',
        email: 'hello@example.com'
    }
}

export const projects: Project[] = [
    {
        id: '1',
        name: 'AdoruWorld Blog',
        description: '口袋妖怪风格的像素艺术个人博客，使用Vue 3和Tailwind CSS构建。',
        tech: ['Vue 3', 'TypeScript', 'Tailwind CSS', 'Vite'],
        link: 'https://example.com',
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-blog/600/400',
        status: 'in-progress'
    },
    {
        id: '2',
        name: 'Pixel Adventure',
        description: '一款像素风格的冒险游戏，使用Phaser 3开发。',
        tech: ['Phaser 3', 'TypeScript', 'Aseprite'],
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-game/600/400',
        status: 'in-progress'
    },
    {
        id: '3',
        name: 'Task Manager',
        description: '一个简洁的任务管理应用，支持拖拽排序和标签分类。',
        tech: ['React', 'Node.js', 'MongoDB'],
        link: 'https://example.com',
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-task/600/400',
        status: 'completed'
    },
    {
        id: '4',
        name: 'Weather App',
        description: '天气预报应用，支持多城市切换和天气动画效果。',
        tech: ['Vue 3', 'OpenWeather API'],
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-weather/600/400',
        status: 'archived'
    },
    {
        id: '1',
        name: 'AdoruWorld Blog',
        description: '口袋妖怪风格的像素艺术个人博客，使用Vue 3和Tailwind CSS构建。',
        tech: ['Vue 3', 'TypeScript', 'Tailwind CSS', 'Vite'],
        link: 'https://example.com',
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-blog/600/400',
        status: 'in-progress'
    },
    {
        id: '2',
        name: 'Pixel Adventure',
        description: '一款像素风格的冒险游戏，使用Phaser 3开发。',
        tech: ['Phaser 3', 'TypeScript', 'Aseprite'],
        link: 'https://example.com',
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-game/600/400',
        status: 'in-progress'
    },
    {
        id: '3',
        name: 'Task Manager',
        description: '一个简洁的任务管理应用，支持拖拽排序和标签分类。',
        tech: ['React', 'Node.js', 'MongoDB'],
        link: 'https://example.com',
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-task/600/400',
        status: 'completed'
    },
    {
        id: '4',
        name: 'Weather App',
        description: '天气预报应用，支持多城市切换和天气动画效果。',
        tech: ['Vue 3', 'OpenWeather API'],
        github: 'https://github.com',
        image: 'https://picsum.photos/seed/project-weather/600/400',
        status: 'archived'
    }
]